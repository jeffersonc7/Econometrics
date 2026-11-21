"""Reproduce EDA/SLR sin ejecutar ni modificar notebooks. Publica sólo agregados."""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import json
import math
from pathlib import Path
import urllib.request

import numpy as np
import pandas as pd
import statsmodels.api as sm
from scipy import stats
from contract import validate_public_artifact

ROOT = Path(__file__).resolve().parents[1]
REVISION = 'd8a5794b62c4e5ec1f7f11b41c28d4ac82d47698'
REPO = 'Jefferson7c/Econometrics'
FILES = {
    'data_clean.parquet': '8c59cf438743d06e2e1da2f00ae83575a159a353eb33e829259992115fa3e1a7',
    'enemdu_persona_tics_2025_07.csv': 'a7071161a63c18cdbb4b6c48e06103c357baf06b961df47259c1d9959dc689ff',
}


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def download(source: Path) -> None:
    """Sólo por CLI explícita; nunca al servir HTTP. Sin tokens."""
    source.mkdir(parents=True, exist_ok=True)
    for name, expected in FILES.items():
        target = source / name
        if target.exists() and digest(target) == expected:
            continue
        url = f'https://huggingface.co/datasets/{REPO}/resolve/{REVISION}/{name}'
        with urllib.request.urlopen(url, timeout=90) as response:
            body = response.read()
        if hashlib.sha256(body).hexdigest() != expected:
            raise ValueError(f'El hash de {name} no coincide con la revisión fijada')
        target.write_bytes(body)


def load_sources(source: Path) -> pd.DataFrame:
    for name, expected in FILES.items():
        target = source / name
        if not target.is_file():
            raise ValueError(f'Falta {name}. Ejecute pipeline.py --download')
        if digest(target) != expected:
            raise ValueError(f'La fuente {name} cambió: no se publican resultados')
    clean = pd.read_parquet(source / 'data_clean.parquet')
    raw = pd.read_csv(source / 'enemdu_persona_tics_2025_07.csv', sep=';', low_memory=False)
    aux = raw[['id_persona', 'periodo', 'p03', 'empleo', 'pt3a']].copy()
    for col in ['id_persona', 'periodo', 'empleo', 'pt3a']:
        aux[col] = aux[col].astype('string').str.strip()
    data = clean.merge(aux, on=['id_persona', 'periodo'], how='left', validate='one_to_one', indicator=True)
    if not data['_merge'].eq('both').all() or data['p03'].isna().any():
        raise ValueError('Existen personas sin correspondencia en el CSV original')
    if not data['periodo'].eq('202507').all() or len(data) != 27509:
        raise ValueError('El periodo o el tamaño de la base cambió')
    if data.duplicated(['id_persona', 'periodo']).any():
        raise ValueError('Identificadores persona-periodo duplicados')
    weights = data['fexp'].to_numpy(dtype=float)
    if not (np.isfinite(weights).all() and (weights > 0).all()):
        raise ValueError('Factores de expansión inválidos')
    if data[['estrato', 'upm']].isna().any().any():
        raise ValueError('Faltan identificadores del diseño muestral')
    return data.drop(columns='_merge')


def select_sample(data: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    employed = data.loc[data['empleo'].eq('1') & data['p03'].ge(15)].copy()
    complete = employed.dropna(subset=['pt3b', 'ingrl']).copy()
    sample = complete.loc[complete['pt3a'].eq('1')].copy()
    if len(sample) < 3 or sample['pt3b'].nunique() < 2:
        raise ValueError('Muestra insuficiente para estimar la regresión')
    return employed, complete, sample


def fit_model(sample: pd.DataFrame):
    x = sm.add_constant(sample['pt3b'].astype(float))
    return sm.OLS(sample['ingrl'].astype(float), x).fit(
        cov_type='cluster', cov_kwds={'groups': sample['upm']}, use_t=True
    )


def binned_by_hours(hours: np.ndarray, values: np.ndarray, edges: np.ndarray) -> list[dict]:
    """Celdas agregadas; np.histogram incluye el máximo en el último intervalo."""
    rows = []
    for hour in range(int(hours.max()) + 1):
        counts, _ = np.histogram(values[hours == hour], bins=edges)
        rows.extend(dict(hours=hour, lower=float(low), upper=float(high), n=int(count))
                    for low, high, count in zip(edges[:-1], edges[1:], counts))
    return rows


def diagnostic_aggregates(sample: pd.DataFrame, model, cook: np.ndarray) -> dict:
    """Diagnósticos de la misma recta MCO; nunca expone residuos individuales."""
    x = sample['pt3b'].to_numpy(dtype=float)
    residuals = np.asarray(model.resid, dtype=float)
    fitted = np.asarray(model.fittedvalues, dtype=float)
    n = len(sample)
    ser = float(model.mse_resid ** .5)
    residual_counts, residual_edges = np.histogram(residuals, bins=28)
    # La banda es puntual para la media lineal, con la covarianza UPM del modelo.
    covariance = np.asarray(model.cov_params(), dtype=float)
    df_inference = int(model.df_resid_inference)
    critical = float(stats.t.ppf(.975, df_inference))
    grid = np.linspace(float(x.min()), float(x.max()), 181)
    design_grid = np.column_stack([np.ones(len(grid)), grid])
    mean = design_grid @ np.asarray(model.params)
    mean_se = np.sqrt(np.maximum(np.einsum('ij,jk,ik->i', design_grid, covariance, design_grid), 0))
    classical = sm.OLS(sample['ingrl'].astype(float), sm.add_constant(sample['pt3b'].astype(float))).fit(use_t=True)
    hc3 = classical.get_robustcov_results(cov_type='HC3', use_t=True)
    comparison = []
    for method, fit in [('Convencional', classical), ('HC3', hc3), ('Agrupado por UPM', model)]:
        interval = np.asarray(fit.conf_int())[1]
        comparison.append(dict(method=method, se=float(np.asarray(fit.bse)[1]),
                               ci_low=float(interval[0]), ci_high=float(interval[1])))
    # Cuantiles agregados: 99 puntos, sin valores ordenados individuales/extremos.
    probabilities = np.arange(1, 100) / 100
    empirical = np.quantile(residuals / ser, probabilities)
    theoretical = stats.norm.ppf(probabilities)
    positive_cook = cook[cook > 0]
    if len(positive_cook) == 0:
        cook_edges = np.linspace(0, 1, 29)
    elif np.any(cook == 0):
        cook_edges = np.r_[0., np.geomspace(positive_cook.min(), max(positive_cook.max(), positive_cook.min() * (1 + 1e-6)), 28)]
    else:
        cook_edges = np.geomspace(cook.min(), max(cook.max(), cook.min() * (1 + 1e-6)), 29)
    cook_counts, _ = np.histogram(cook, bins=cook_edges)
    y = sample['ingrl'].to_numpy(dtype=float)
    return dict(
        fit_band=[dict(hours=float(h), income=float(v), ci_low=float(v-critical*se), ci_high=float(v+critical*se))
                  for h, v, se in zip(grid, mean, mean_se)],
        residual_density=binned_by_hours(x, residuals, residual_edges),
        residual_histogram=[dict(lower=float(lo), upper=float(hi), n=int(count))
                            for lo, hi, count in zip(residual_edges[:-1], residual_edges[1:], residual_counts)],
        qq=[dict(theoretical=float(a), empirical=float(b)) for a, b in zip(theoretical, empirical)],
        covariance=covariance.tolist(), t_critical=critical, df_inference=df_inference,
        ee_comparison=comparison, residual_mean=float(residuals.mean()),
        residual_skew=float(stats.skew(residuals, bias=False)),
        residual_kurtosis=float(stats.kurtosis(residuals, fisher=False, bias=False)),
        cook_histogram=[dict(lower=float(lo), upper=float(hi), n=int(count))
                        for lo, hi, count in zip(cook_edges[:-1], cook_edges[1:], cook_counts)],
        rmse=float(np.sqrt(np.mean(residuals ** 2))), mae=float(np.mean(np.abs(residuals))),
        adjusted_r_squared=float(model.rsquared_adj),
        sse=float(residuals @ residuals), sst=float(np.sum((y-y.mean()) ** 2)),
        ssr=float(np.sum((fitted-y.mean()) ** 2)),
    )


def exploratory_visuals(sample: pd.DataFrame) -> dict:
    """Resúmenes gráficos adicionales del dominio ya aprobado, sin ponderación."""
    x = sample['pt3b'].to_numpy(dtype=float)
    y = sample['ingrl'].to_numpy(dtype=float)
    edges = np.array([0, 100, 250, 500, 750, 1000, 1500, 3000, 5000, 10000, 17001], dtype=float)
    boxes = []
    for i, (label, group) in enumerate(sample.groupby('tramo', observed=True)):
        values = group['ingrl'].to_numpy(dtype=float)
        p10, q1, median, q3, p90 = np.quantile(values, [.1, .25, .5, .75, .9])
        boxes.append(dict(key=str(i), label=str(label), n=len(values), q1=float(q1), median=float(median),
                          q3=float(q3), p10=float(p10), p90=float(p90), mean=float(values.mean())))
    thresholds = np.quantile(y, np.arange(101) / 100)
    return dict(
        density=binned_by_hours(x, y, edges), boxplots=boxes,
        income_cdf=[dict(income=float(threshold), share=float(np.mean(y <= threshold))) for threshold in thresholds],
        percentiles=[dict(p=p, income=float(np.quantile(y, p/100)), hours=float(np.quantile(x, p/100)))
                     for p in [10, 25, 50, 75, 90, 99]],
    )


def generate(source: Path = ROOT / 'data/source') -> dict:
    data = load_sources(source)
    employed, complete, sample = select_sample(data)
    # Bloquear publicación si la especificación ya no reproduce el resultado fuente.
    if [len(employed), len(complete), len(sample)] != [13299, 10091, 9881]:
        raise ValueError('La selección no coincide con los notebooks auditados')
    model = fit_model(sample)
    if not math.isclose(model.params['pt3b'], 61.3563899864, rel_tol=1e-9):
        raise ValueError('La regresión no reproduce el notebook: publicación bloqueada')
    x = sample['pt3b'].to_numpy(dtype=float)
    y = sample['ingrl'].to_numpy(dtype=float)
    w = sample['fexp'].to_numpy(dtype=float)
    xc, yc = x - np.average(x, weights=w), y - np.average(y, weights=w)
    weighted_r = np.sum(w * xc * yc) / np.sqrt(np.sum(w * xc**2) * np.sum(w * yc**2))
    overview = dict(
        n=len(sample), income_mean=float(y.mean()), income_median=float(np.median(y)),
        hours_mean=float(x.mean()), hours_median=float(np.median(x)),
        income_weighted_mean=float(np.average(y, weights=w)),
        hours_weighted_mean=float(np.average(x, weights=w)),
        pearson=float(np.corrcoef(x, y)[0, 1]), spearman=float(sample[['pt3b', 'ingrl']].rank().corr().iloc[0, 1]),
        weighted_pearson=float(weighted_r), zero_hours_n=int((x == 0).sum()),
        zero_income_n=int((y == 0).sum()), income_p99=float(np.quantile(y, .99)),
        income_max=float(y.max()), hours_max=float(x.max()),
    )
    labels = ['0–1', '2–3', '4–5', '6–8', '9 o más']
    sample['tramo'] = pd.cut(sample['pt3b'], [-1, 1, 3, 5, 8, np.inf], labels=labels)
    groups = [dict(key=str(i), label=label, n=len(group), income_mean=float(group['ingrl'].mean()),
                   income_median=float(group['ingrl'].median()), hours_mean=float(group['pt3b'].mean()))
              for i, (label, group) in enumerate(sample.groupby('tramo', observed=True))]
    hours = [dict(hours=h, n=int((x == h).sum())) for h in range(int(x.max()) + 1)]
    edges = [0, 100, 250, 500, 750, 1000, 1500, 3000, np.inf]
    income = [dict(label=f'{low}–<{high}' if np.isfinite(high) else f'{low} o más',
                   lower=low, upper=high if np.isfinite(high) else None,
                   n=int(((y >= low) & (y < high)).sum())) for low, high in zip(edges[:-1], edges[1:])]
    availability = [
        dict(label='Horas e ingreso disponibles', n=len(complete)),
        dict(label='Falta al menos una respuesta', n=len(employed) - len(complete)),
    ]
    coefficients = [dict(term=str(term), estimate=float(model.params[term]), se=float(model.bse[term]),
                         t=float(model.tvalues[term]), p=float(model.pvalues[term]),
                         ci_low=float(model.conf_int().loc[term, 0]), ci_high=float(model.conf_int().loc[term, 1]))
                    for term in model.params.index]
    variance_model = sm.OLS(model.resid**2, sm.add_constant(sample['pt3b'].astype(float))).fit(
        cov_type='cluster', cov_kwds={'groups': sample['upm']}, use_t=True)
    cook = model.get_influence().cooks_distance[0]
    retained = sample.loc[cook <= 4 / len(sample)].copy()
    sensitivity = fit_model(retained)
    spread = pd.DataFrame({'hours': x, 'residual': np.asarray(model.resid)}).groupby('hours')['residual'].agg(['size', 'std'])
    spread = spread.loc[spread['size'].ge(30)]
    model_data = dict(
        n=len(sample), clusters=int(sample['upm'].nunique()), households=int(sample['id_hogar'].nunique()),
        strata=int(sample['estrato'].nunique()), r_squared=float(model.rsquared), ser=float(model.mse_resid**.5),
        x_variance=float(sample['pt3b'].var()), coefficients=coefficients,
        heteroskedasticity_p=float(variance_model.pvalues['pt3b']), cook_flagged_n=int((cook > 4 / len(sample)).sum()),
        sensitivity=dict(n=len(retained), slope=float(sensitivity.params['pt3b']),
                         ci_low=float(sensitivity.conf_int().loc['pt3b', 0]), ci_high=float(sensitivity.conf_int().loc['pt3b', 1])),
        residual_spread=[dict(hours=int(h), n=int(row['size']), std=float(row['std'])) for h, row in spread.iterrows()],
        fitted=[dict(hours=h, income=float(model.params['const'] + model.params['pt3b'] * h)) for h in range(int(x.max()) + 1)],
        diagnostics=diagnostic_aggregates(sample, model, cook),
    )
    result = dict(data=dict(
        selection=[dict(label=label, n=n) for label, n in zip(
            ['Base limpia', 'Ocupados de 15 años o más', 'Horas e ingreso disponibles', 'Uso diario y datos disponibles'],
            [len(data), len(employed), len(complete), len(sample)])],
        overview=overview, groups=groups, hours=hours, income=income, availability=availability, model=model_data,
        visuals=exploratory_visuals(sample),
    ), meta=dict(
        schema_version='1.0', generated_at=datetime.now(timezone.utc).isoformat(),
        source='INEC · ENEMDU TIC · julio de 2025', revision=REVISION,
        clean_sha256=FILES['data_clean.parquet'], raw_sha256=FILES['enemdu_persona_tics_2025_07.csv'],
        population='Ocupados de 15 años o más, usuarios diarios de internet, con horas e ingreso disponibles',
        period='Julio de 2025', income_period='Junio de 2025', weight='Sin ponderar; fexp sólo en medias y correlación ponderadas explícitas',
        n=len(sample), source_url=f'https://huggingface.co/datasets/{REPO}/tree/{REVISION}',
        license_status='Repositorio HF: MIT declarada. Condiciones de fuente INEC deben conservarse; sólo se publican agregados.',
    ))
    validate_public_artifact(result)
    validate_artifact(result)
    return result


def validate_artifact(result: dict) -> None:
    if result['meta']['schema_version'] != '1.0':
        raise ValueError('Versión de datos incompatible')
    payload = result['data']
    n = payload['overview']['n']
    if n != result['meta']['n'] or n != payload['model']['n'] or n <= 0:
        raise ValueError('Denominadores incompatibles')
    for key in ['groups', 'hours', 'income']:
        if sum(group['n'] for group in payload[key]) != n:
            raise ValueError(f'El agregado {key} no conserva todas las observaciones')
    if sum(row['n'] for row in payload['availability']) != payload['selection'][1]['n']:
        raise ValueError('La disponibilidad no conserva el denominador de ocupados')
    # JSON estricto: rechazar NaN/Infinity y tipos no serializables.
    json.dumps(result, allow_nan=False)


def main() -> None:
    parser = argparse.ArgumentParser(description='Reproducir agregados de ENEMDU para el dashboard')
    parser.add_argument('--source', type=Path, default=ROOT / 'data/source')
    parser.add_argument('--output', type=Path, default=ROOT / 'frontend/public/data/dashboard.json')
    parser.add_argument('--download', action='store_true', help='Descargar fuentes de la revisión fijada')
    args = parser.parse_args()
    if args.download:
        download(args.source)
    artifact = generate(args.source)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    temporary = args.output.with_suffix('.tmp')
    temporary.write_text(json.dumps(artifact, ensure_ascii=False, indent=2, allow_nan=False) + '\n', encoding='utf-8')
    temporary.replace(args.output)
    print(f'Agregados verificados: {artifact["meta"]["n"]} observaciones → {args.output}')


if __name__ == '__main__':
    main()
