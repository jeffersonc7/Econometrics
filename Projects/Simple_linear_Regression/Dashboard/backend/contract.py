"""Contrato público de agregados; validación sin dependencias científicas."""
import math


def validate_public_artifact(value):
    def fail():
        raise ValueError('El archivo de agregados no cumple el contrato v1')

    def number(v, count=False):
        if isinstance(v, bool) or not isinstance(v, (int, float)) or not math.isfinite(v):
            fail()
        if count and (v < 0 or not isinstance(v, int)):
            fail()

    def numeric(record, names):
        for name in names:
            number(record[name])

    def close(a, b):
        return math.isclose(a, b, rel_tol=1e-8, abs_tol=1e-7)

    def histogram(rows, expected_n):
        if not isinstance(rows, list) or not rows:
            fail()
        for i, row in enumerate(rows):
            numeric(row, ['lower', 'upper'])
            number(row['n'], count=True)
            if row['lower'] >= row['upper'] or (i and not close(rows[i-1]['upper'], row['lower'])):
                fail()
        if sum(row['n'] for row in rows) != expected_n:
            fail()

    def density(rows, hour_rows, expected_bins):
        if len(rows) != len(hour_rows) * expected_bins:
            fail()
        for hour_row in hour_rows:
            selected = [row for row in rows if row['hours'] == hour_row['hours']]
            if len(selected) != expected_bins:
                fail()
            histogram(selected, hour_row['n'])
        # Una única rejilla vertical para que el color sea comparable por hora.
        reference = [(r['lower'], r['upper']) for r in rows[:expected_bins]]
        for i in range(0, len(rows), expected_bins):
            if [(r['lower'], r['upper']) for r in rows[i:i+expected_bins]] != reference:
                fail()

    try:
        meta, data = value['meta'], value['data']
        for key in ['generated_at', 'source', 'revision', 'clean_sha256', 'raw_sha256', 'population',
                    'period', 'income_period', 'weight', 'source_url', 'license_status']:
            if not isinstance(meta[key], str) or not meta[key]:
                fail()
        if meta['schema_version'] != '1.0':
            fail()
        n = meta['n']
        number(n, count=True)
        if n == 0:
            fail()
        overview, model = data['overview'], data['model']
        numeric(overview, ['n', 'income_mean', 'income_median', 'hours_mean', 'hours_median',
                          'income_weighted_mean', 'hours_weighted_mean', 'pearson', 'spearman',
                          'weighted_pearson', 'zero_hours_n', 'zero_income_n', 'income_p99', 'income_max', 'hours_max'])
        numeric(model, ['n', 'clusters', 'households', 'strata', 'r_squared', 'ser', 'x_variance',
                        'heteroskedasticity_p', 'cook_flagged_n'])
        if overview['n'] != n or model['n'] != n:
            fail()
        selection = data['selection']
        if len(selection) != 4 or selection[-1]['n'] != n:
            fail()
        for row in selection:
            number(row['n'], count=True)
            if not isinstance(row['label'], str):
                fail()
        if any(selection[i]['n'] < selection[i+1]['n'] for i in range(3)):
            fail()
        for key in ['groups', 'hours', 'income', 'availability']:
            rows = data[key]
            if not isinstance(rows, list) or not rows:
                fail()
            for row in rows:
                number(row['n'], count=True)
            if sum(row['n'] for row in rows) != (selection[1]['n'] if key == 'availability' else n):
                fail()
        for row in data['groups']:
            if not isinstance(row['key'], str) or not isinstance(row['label'], str):
                fail()
            numeric(row, ['income_mean', 'income_median', 'hours_mean'])
        for row in data['hours']:
            number(row['hours'])
        for row in data['income']:
            number(row['lower'])
            if row['upper'] is not None:
                number(row['upper'])
                if row['upper'] <= row['lower']:
                    fail()
        if len(model['coefficients']) != 2:
            fail()
        for row in model['coefficients']:
            numeric(row, ['estimate', 'se', 't', 'p', 'ci_low', 'ci_high'])
            if not row['ci_low'] <= row['estimate'] <= row['ci_high'] or not 0 <= row['p'] <= 1 or row['se'] <= 0:
                fail()
        if [row['term'] for row in model['coefficients']] != ['const', 'pt3b']:
            fail()
        numeric(model['sensitivity'], ['n', 'slope', 'ci_low', 'ci_high'])
        for row in model['residual_spread']:
            numeric(row, ['hours', 'n', 'std'])
            if row['n'] < 30:
                fail()
        for row in model['fitted']:
            numeric(row, ['hours', 'income'])
        visuals, diagnostics = data['visuals'], model['diagnostics']
        density(visuals['density'], data['hours'], 10)
        if len(visuals['boxplots']) != len(data['groups']):
            fail()
        for row, group in zip(visuals['boxplots'], data['groups']):
            numeric(row, ['q1', 'median', 'q3', 'p10', 'p90', 'mean'])
            number(row['n'], count=True)
            if row['key'] != group['key'] or row['label'] != group['label'] or row['n'] != group['n']:
                fail()
            if not row['p10'] <= row['q1'] <= row['median'] <= row['q3'] <= row['p90']:
                fail()
            if not close(row['median'], group['income_median']) or not close(row['mean'], group['income_mean']):
                fail()
        cdf = visuals['income_cdf']
        if len(cdf) != 101 or not close(cdf[-1]['share'], 1):
            fail()
        for i, row in enumerate(cdf):
            numeric(row, ['income', 'share'])
            if not 0 <= row['share'] <= 1:
                fail()
            if i and (row['income'] < cdf[i-1]['income'] or row['share'] < cdf[i-1]['share']):
                fail()
        if [r['p'] for r in visuals['percentiles']] != [10, 25, 50, 75, 90, 99]:
            fail()
        for row in visuals['percentiles']:
            numeric(row, ['p', 'income', 'hours'])
        density(diagnostics['residual_density'], data['hours'], 28)
        histogram(diagnostics['residual_histogram'], n)
        if len(diagnostics['residual_histogram']) != 28:
            fail()
        for i, histogram_row in enumerate(diagnostics['residual_histogram']):
            cells = diagnostics['residual_density'][i::28]
            if sum(row['n'] for row in cells) != histogram_row['n']:
                fail()
            if any(not close(row['lower'], histogram_row['lower']) or not close(row['upper'], histogram_row['upper']) for row in cells):
                fail()
        histogram(diagnostics['cook_histogram'], n)
        if len(diagnostics['cook_histogram']) != 28 or diagnostics['cook_histogram'][0]['lower'] < 0:
            fail()
        if len(diagnostics['qq']) != 99:
            fail()
        for i, row in enumerate(diagnostics['qq']):
            numeric(row, ['theoretical', 'empirical'])
            if i and (row['theoretical'] <= diagnostics['qq'][i-1]['theoretical'] or row['empirical'] < diagnostics['qq'][i-1]['empirical']):
                fail()
        numeric(diagnostics, ['t_critical', 'df_inference', 'residual_mean', 'residual_skew',
                              'residual_kurtosis', 'rmse', 'mae', 'adjusted_r_squared', 'sse', 'sst', 'ssr'])
        if diagnostics['df_inference'] != model['clusters'] - 1 or diagnostics['t_critical'] <= 0:
            fail()
        covariance = diagnostics['covariance']
        if len(covariance) != 2 or any(len(row) != 2 for row in covariance):
            fail()
        for row in covariance:
            for cell in row:
                number(cell)
        if covariance[0][0] <= 0 or covariance[1][1] <= 0 or not close(covariance[0][1], covariance[1][0]):
            fail()
        if covariance[0][0]*covariance[1][1] < covariance[0][1]**2 - 1e-7:
            fail()
        for i, coefficient in enumerate(model['coefficients']):
            if not close(coefficient['se'] ** 2, covariance[i][i]):
                fail()
        if len(diagnostics['fit_band']) != 181:
            fail()
        b0, b1 = [row['estimate'] for row in model['coefficients']]
        for i, row in enumerate(diagnostics['fit_band']):
            numeric(row, ['hours', 'income', 'ci_low', 'ci_high'])
            h = row['hours']
            if not 0 <= h <= overview['hours_max'] or (i and h <= diagnostics['fit_band'][i-1]['hours']):
                fail()
            variance = covariance[0][0] + 2*h*covariance[0][1] + h*h*covariance[1][1]
            margin = diagnostics['t_critical'] * math.sqrt(max(variance, 0))
            if not close(row['income'], b0+b1*h) or not close(row['ci_low'], row['income']-margin) or not close(row['ci_high'], row['income']+margin):
                fail()
        comparison = diagnostics['ee_comparison']
        if [row['method'] for row in comparison] != ['Convencional', 'HC3', 'Agrupado por UPM']:
            fail()
        for row in comparison:
            numeric(row, ['se', 'ci_low', 'ci_high'])
            if row['se'] <= 0 or not row['ci_low'] <= b1 <= row['ci_high']:
                fail()
        if not close(comparison[-1]['se'], model['coefficients'][1]['se']):
            fail()
        if diagnostics['sse'] <= 0 or diagnostics['sst'] <= 0 or diagnostics['ssr'] < 0:
            fail()
        if not close(diagnostics['sse'] + diagnostics['ssr'], diagnostics['sst']):
            fail()
        if not close(diagnostics['rmse'] ** 2 * n, diagnostics['sse']) or not close(model['ser'] ** 2 * (n-2), diagnostics['sse']):
            fail()
        if not close(model['r_squared'], diagnostics['ssr']/diagnostics['sst']):
            fail()
        if diagnostics['mae'] < 0 or diagnostics['mae'] > diagnostics['rmse'] or abs(diagnostics['residual_mean']) > 1e-6:
            fail()
    except (KeyError, TypeError, IndexError, AttributeError, OverflowError) as error:
        raise ValueError('El archivo de agregados no cumple el contrato v1') from error
