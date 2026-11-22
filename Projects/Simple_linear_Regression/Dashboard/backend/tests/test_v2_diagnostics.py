"""V2: invariantes de inferencia, conservación y rechazo de artefactos incoherentes."""
import copy
import json
import math
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from contract import validate_public_artifact


class V2DiagnosticsTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.artifact = json.loads((Path(__file__).resolve().parents[2] / 'frontend/public/data/dashboard.json').read_text())
        cls.data = cls.artifact['data']
        cls.model = cls.data['model']
        cls.d = cls.model['diagnostics']

    def test_public_grids_conserve_each_hour_and_both_tails(self):
        for key, rows, bins in [('ingreso', self.data['visuals']['density'], 10),
                                ('residuo', self.d['residual_density'], 28)]:
            with self.subTest(key=key):
                self.assertEqual(sum(r['n'] for r in rows), 9881)
                self.assertEqual(len(rows), 19*bins)
                for h in self.data['hours']:
                    cells = [r for r in rows if r['hours'] == h['hours']]
                    self.assertEqual(sum(r['n'] for r in cells), h['n'])
                self.assertGreater(sum(r['n'] for r in rows if r['lower'] == rows[0]['lower']), 0)
                self.assertGreater(sum(r['n'] for r in rows if r['upper'] == rows[-1]['upper']), 0)
        self.assertEqual(sum(r['n'] for r in self.d['residual_histogram']), 9881)
        self.assertEqual(sum(r['n'] for r in self.d['cook_histogram']), 9881)
        self.assertEqual(len(self.d['residual_histogram']), 28)
        for i, row in enumerate(self.d['residual_histogram']):
            self.assertEqual(row['n'], sum(r['n'] for r in self.d['residual_density'][i::28]))

    def test_mean_band_uses_covariance_not_prediction_error(self):
        cov = self.d['covariance']
        critical = self.d['t_critical']
        self.assertEqual(self.d['df_inference'], 1285)
        self.assertAlmostEqual(critical, 1.9618118205524082, places=10)
        for row in self.d['fit_band']:
            x = row['hours']
            expected_se = math.sqrt(cov[0][0] + 2*x*cov[0][1] + x*x*cov[1][1])
            self.assertAlmostEqual((row['ci_high'] - row['ci_low']) / (2*critical), expected_se, places=8)
            # La banda puntual no suma SER² como un intervalo individual.
            self.assertLess((row['ci_high'] - row['ci_low']) / (2*critical), self.model['ser'])
        cluster = self.model['coefficients'][1]
        self.assertAlmostEqual(cov[1][1], cluster['se']**2, places=10)

    def test_ss_decomposition_and_error_scales(self):
        n, d = self.model['n'], self.d
        self.assertAlmostEqual((d['sse'] + d['ssr']) / d['sst'], 1, places=12)
        self.assertAlmostEqual(d['rmse']**2*n / d['sse'], 1, places=12)
        self.assertAlmostEqual(self.model['ser']**2*(n-2) / d['sse'], 1, places=12)
        self.assertAlmostEqual(d['ssr']/d['sst'], self.model['r_squared'], places=12)
        self.assertLess(d['rmse'], self.model['ser'])
        self.assertLess(d['mae'], d['rmse'])
        self.assertAlmostEqual(d['residual_mean'], 0, places=8)
        self.assertAlmostEqual(d['adjusted_r_squared'], 1-(1-self.model['r_squared'])*(n-1)/(n-2), places=12)

    def test_quantiles_cdf_and_qq_are_ordered_and_finite(self):
        boxes = self.data['visuals']['boxplots']
        for b, group in zip(boxes, self.data['groups']):
            self.assertEqual(b['median'], group['income_median'])
            self.assertEqual(b['n'], group['n'])
            self.assertLessEqual(b['p10'], b['q1'])
            self.assertLessEqual(b['q1'], b['median'])
            self.assertLessEqual(b['median'], b['q3'])
            self.assertLessEqual(b['q3'], b['p90'])
        p50 = next(r for r in self.data['visuals']['percentiles'] if r['p'] == 50)
        self.assertEqual((p50['income'], p50['hours']), (474, 3))
        cdf = self.data['visuals']['income_cdf']
        self.assertEqual(cdf[0]['income'], 0)
        self.assertAlmostEqual(cdf[0]['share'], 119/9881, places=12)
        self.assertEqual(cdf[-1], {'income': 17000., 'share': 1.})
        self.assertTrue(all(a['share'] <= b['share'] for a, b in zip(cdf, cdf[1:])))
        qq = self.d['qq']
        self.assertEqual(len(qq), 99)
        self.assertAlmostEqual(qq[0]['theoretical'], -2.32634787404, places=8)
        self.assertAlmostEqual(qq[-1]['theoretical'], 2.32634787404, places=8)
        self.assertTrue(all(math.isfinite(r[k]) for r in qq for k in r))

    def test_ee_comparison_preserves_slope_and_cluster_result(self):
        slope = self.model['coefficients'][1]
        self.assertEqual([r['method'] for r in self.d['ee_comparison']], ['Convencional', 'HC3', 'Agrupado por UPM'])
        for row in self.d['ee_comparison']:
            self.assertAlmostEqual((row['ci_low'] + row['ci_high'])/2, slope['estimate'], places=10)
        row = self.d['ee_comparison'][-1]
        for key in ['se', 'ci_low', 'ci_high']:
            self.assertEqual(row[key], slope[key])

    def test_difference_interval_for_negative_zero_and_positive_delta(self):
        slope = self.model['coefficients'][1]
        critical = self.d['t_critical']
        for delta in [-3., 0., 3.]:
            estimate = delta*slope['estimate']
            margin = critical*abs(delta)*slope['se']
            low, high = estimate-margin, estimate+margin
            ordered_endpoints = sorted([delta*slope['ci_low'], delta*slope['ci_high']])
            self.assertLessEqual(low, high)
            self.assertAlmostEqual(low, ordered_endpoints[0], places=10)
            self.assertAlmostEqual(high, ordered_endpoints[1], places=10)

    def test_corrupt_v2_statistics_are_rejected(self):
        mutations = [
            lambda a: a['data']['visuals']['density'][0].update(n=999),
            lambda a: a['data']['model']['diagnostics']['covariance'][1].__setitem__(1, 1),
            lambda a: a['data']['model']['diagnostics']['fit_band'][0].update(ci_high=99999),
            lambda a: a['data']['model']['diagnostics'].update(sse=1),
            lambda a: a['data']['visuals']['income_cdf'][50].update(share=-.1),
            lambda a: a['data']['model']['diagnostics']['qq'][0].update(empirical=float('nan')),
        ]
        for mutation in mutations:
            with self.subTest(mutation=mutation):
                broken = copy.deepcopy(self.artifact)
                mutation(broken)
                with self.assertRaises(ValueError):
                    validate_public_artifact(broken)
        validate_public_artifact(self.artifact)


if __name__ == '__main__':
    unittest.main()
