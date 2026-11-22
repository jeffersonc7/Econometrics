"""Réplica independiente v2: originales + statsmodels, sin importar pipeline.

Verifica los nuevos números públicos contra una estimación separada y la muestra
fuente; no comparte funciones productoras ni constantes de resultados v2.
"""
import json
from pathlib import Path
import unittest

import numpy as np
import pandas as pd
from scipy import stats
import statsmodels.api as sm

ROOT = Path(__file__).resolve().parents[2]


class IndependentV2Review(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.artifact = json.loads((ROOT / 'frontend/public/data/dashboard.json').read_text())
        cls.data = cls.artifact['data']
        cls.visuals = cls.data['visuals']
        cls.diag = cls.data['model']['diagnostics']
        # Leer la fuente original en DataScience; nunca escribir allí ni ejecutar notebooks.
        clean = pd.read_parquet(ROOT.parent / 'DataScience/data/processed/data_clean.parquet')
        raw = pd.read_csv(ROOT / 'data/source/enemdu_persona_tics_2025_07.csv', sep=';', low_memory=False,
                          usecols=['id_persona', 'periodo', 'p03', 'empleo', 'pt3a'])
        for col in ['id_persona', 'periodo', 'empleo', 'pt3a']:
            raw[col] = raw[col].astype('string').str.strip()
        joined = clean.merge(raw, on=['id_persona', 'periodo'], validate='one_to_one')
        sample = joined.loc[joined['empleo'].eq('1') & joined['p03'].ge(15)
                            & joined['pt3a'].eq('1') & joined['pt3b'].notna() & joined['ingrl'].notna()]
        cls.n = len(sample)
        cls.x = sample['pt3b'].to_numpy(float)
        cls.y = sample['ingrl'].to_numpy(float)
        cls.design = sm.add_constant(cls.x)
        cls.ordinary = sm.OLS(cls.y, cls.design).fit(use_t=True)
        cls.cluster = sm.OLS(cls.y, cls.design).fit(cov_type='cluster',
                          cov_kwds={'groups': sample['upm']}, use_t=True)
        cls.residual = np.asarray(cls.cluster.resid)

    def test_density_all_cells_from_original_observations(self):
        self.assertEqual(self.n, 9881)
        edges = np.array([0, 100, 250, 500, 750, 1000, 1500, 3000, 5000, 10000, 17001], float)
        expected, _, _ = np.histogram2d(self.x, self.y, bins=[np.arange(-.5, 19.5), edges])
        cells = self.visuals['density']
        self.assertEqual(len(cells), 19 * 10)
        actual = {(row['hours'], row['lower'], row['upper']): row['n'] for row in cells}
        self.assertEqual(len(actual), len(cells))
        for h in range(19):
            for j in range(10):
                self.assertEqual(actual[(h, edges[j], edges[j+1])], int(expected[h, j]))
        self.assertEqual(sum(actual.values()), self.n)
        self.assertEqual(sum(row['n'] for row in cells if row['hours'] == 17), 0)

    def test_boxplots_are_quantiles_not_arbitrary_whiskers(self):
        masks = [self.x <= 1, (self.x >= 2) & (self.x <= 3),
                 (self.x >= 4) & (self.x <= 5), (self.x >= 6) & (self.x <= 8), self.x >= 9]
        self.assertEqual(len(self.visuals['boxplots']), len(masks))
        for box, mask in zip(self.visuals['boxplots'], masks):
            values = self.y[mask]
            self.assertEqual(box['n'], len(values))
            np.testing.assert_allclose([box[k] for k in ['p10', 'q1', 'median', 'q3', 'p90']],
                                       np.quantile(values, [.1, .25, .5, .75, .9]), rtol=1e-12)
            self.assertAlmostEqual(box['mean'], values.mean(), places=10)

    def test_cdf_uses_empirical_counts_including_ties_and_zero(self):
        rows = self.visuals['income_cdf']
        thresholds = np.quantile(self.y, np.arange(101) / 100)
        sorted_income = np.sort(self.y)
        self.assertEqual(len(rows), 101)
        np.testing.assert_allclose([r['income'] for r in rows], thresholds, rtol=1e-12)
        expected_share = np.searchsorted(sorted_income, thresholds, side='right') / self.n
        np.testing.assert_allclose([r['share'] for r in rows], expected_share, rtol=1e-12)
        self.assertAlmostEqual(rows[0]['share'], np.count_nonzero(self.y == 0) / self.n)
        self.assertEqual(rows[-1]['share'], 1)
        for a, b in zip(rows[:-1], rows[1:]):
            self.assertLessEqual(a['income'], b['income'])
            self.assertLessEqual(a['share'], b['share'])
            if a['income'] == b['income']:
                self.assertEqual(a['share'], b['share'])

    def test_percentiles_match_source(self):
        self.assertEqual([r['p'] for r in self.visuals['percentiles']], [10, 25, 50, 75, 90, 99])
        for row in self.visuals['percentiles']:
            self.assertAlmostEqual(row['income'], np.quantile(self.y, row['p']/100), places=10)
            self.assertAlmostEqual(row['hours'], np.quantile(self.x, row['p']/100), places=10)

    def test_mean_band_from_full_cluster_covariance_not_prediction_error(self):
        d = self.diag
        covariance = np.asarray(self.cluster.cov_params())
        np.testing.assert_allclose(d['covariance'], covariance, rtol=1e-11)
        self.assertEqual(d['df_inference'], 1285)
        critical = stats.t.ppf(.975, d['df_inference'])
        self.assertAlmostEqual(d['t_critical'], critical, places=12)
        rows = d['fit_band']
        self.assertEqual(len(rows), 181)
        self.assertEqual(rows[0]['hours'], 0)
        self.assertEqual(rows[-1]['hours'], 18)
        for row in rows:
            vector = np.array([1, row['hours']])
            fitted = vector @ self.cluster.params
            half_width = critical * np.sqrt(vector @ covariance @ vector)
            np.testing.assert_allclose([row['income'], row['ci_low'], row['ci_high']],
                                      [fitted, fitted-half_width, fitted+half_width], rtol=1e-11)
        # Una banda puntual de media no debe incorporar SER como una predicción individual.
        self.assertLess(rows[0]['ci_high'] - rows[0]['ci_low'], self.cluster.mse_resid**.5)

    def test_residual_heatmap_and_histogram_same_28_bins_and_all_people(self):
        d = self.diag
        counts, edges = np.histogram(self.residual, bins=28)
        rows = d['residual_histogram']
        self.assertEqual(len(rows), 28)
        self.assertEqual(len(d['residual_density']), 19*28)
        np.testing.assert_allclose([r['lower'] for r in rows], edges[:-1], atol=1e-9)
        np.testing.assert_allclose([r['upper'] for r in rows], edges[1:], atol=1e-9)
        self.assertEqual([r['n'] for r in rows], counts.tolist())
        matrix, _, _ = np.histogram2d(self.x, self.residual, bins=[np.arange(-.5,19.5),edges])
        cells = {(r['hours'], r['lower'], r['upper']): r['n'] for r in d['residual_density']}
        self.assertEqual(len(cells), 19*28)
        for h in range(19):
            for j in range(28):
                # Los bordes se comparan por orden para tolerar diferencias numéricas minúsculas.
                row = d['residual_density'][h*28+j]
                self.assertEqual(row['hours'], h)
                self.assertAlmostEqual(row['lower'], edges[j], places=8)
                self.assertAlmostEqual(row['upper'], edges[j+1], places=8)
                self.assertEqual(row['n'], int(matrix[h,j]))
        self.assertEqual(sum(counts), self.n)
        self.assertEqual(sum(cells.values()), self.n)

    def test_qq_uses_finite_quantiles_of_ser_standardized_residuals(self):
        rows = self.diag['qq']
        self.assertEqual(len(rows), 99)
        probabilities = np.arange(1,100) / 100
        theoretical = stats.norm.ppf(probabilities)
        empirical = np.quantile(self.residual / self.cluster.mse_resid**.5, probabilities)
        np.testing.assert_allclose([r['theoretical'] for r in rows], theoretical, rtol=1e-11)
        np.testing.assert_allclose([r['empirical'] for r in rows], empirical, rtol=1e-11)
        self.assertTrue(np.isfinite([*theoretical, *empirical]).all())

    def test_standard_error_comparison_from_separate_statsmodels_fits(self):
        fits = [self.ordinary, self.ordinary.get_robustcov_results(cov_type='HC3', use_t=True), self.cluster]
        rows = self.diag['ee_comparison']
        self.assertEqual([r['method'] for r in rows], ['Convencional', 'HC3', 'Agrupado por UPM'])
        for row, fit in zip(rows, fits):
            self.assertAlmostEqual(row['se'], fit.bse[1], places=10)
            np.testing.assert_allclose([row['ci_low'],row['ci_high']], np.asarray(fit.conf_int())[1], rtol=1e-11)

    def test_error_metrics_and_sums_of_squares_against_original_fit(self):
        d = self.diag
        residual = self.residual
        sse = np.sum(residual**2)
        sst = np.sum((self.y - self.y.mean())**2)
        self.assertAlmostEqual(d['sse'] / sse, 1, places=12)
        self.assertAlmostEqual(d['sst'] / sst, 1, places=12)
        self.assertAlmostEqual((d['sse'] + d['ssr']) / d['sst'], 1, places=12)
        self.assertAlmostEqual(d['rmse'], np.sqrt(np.mean(residual**2)), places=10)
        self.assertAlmostEqual(d['mae'], np.mean(np.abs(residual)), places=10)
        self.assertAlmostEqual(d['adjusted_r_squared'], self.cluster.rsquared_adj, places=12)
        self.assertLess(d['rmse'], self.data['model']['ser'])
        self.assertAlmostEqual(d['residual_mean'], residual.mean(), places=10)
        self.assertAlmostEqual(d['residual_skew'], stats.skew(residual,bias=False), places=10)
        self.assertAlmostEqual(d['residual_kurtosis'], stats.kurtosis(residual,fisher=False,bias=False), places=10)

    def test_cook_histogram_replicates_influence_and_keeps_maximum(self):
        cook = self.cluster.get_influence().cooks_distance[0]
        rows = self.diag['cook_histogram']
        edges = np.array([rows[0]['lower'], *[r['upper'] for r in rows]])
        self.assertEqual(len(rows), 28)
        self.assertTrue((np.diff(edges)>0).all())
        self.assertLessEqual(edges[0], cook.min())
        self.assertGreaterEqual(edges[-1], cook.max())
        expected, _ = np.histogram(cook, bins=edges)
        self.assertEqual([r['n'] for r in rows], expected.tolist())
        self.assertEqual(sum(expected), self.n)

    def test_public_artifact_has_no_individual_identifiers_or_residual_records(self):
        serialized = json.dumps(self.artifact)
        for forbidden in ['id_persona','id_hogar','id_vivienda','ingrl_original','conglomerado']:
            self.assertNotIn(forbidden,serialized)
        self.assertEqual(self.artifact['meta']['revision'], 'd8a5794b62c4e5ec1f7f11b41c28d4ac82d47698')
        self.assertFalse(any(key in self.diag for key in ['residuals','observations','person_records']))
        # JSON estándar, incluso en nuevos diagnósticos y cuantiles.
        json.dumps(self.artifact, allow_nan=False)


if __name__ == '__main__':
    unittest.main()
