"""Pruebas de evidencia contra outputs guardados, conservación y errores reales."""
import copy
import importlib.util
import json
from pathlib import Path
import tempfile
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import unittest

SPEC = importlib.util.spec_from_file_location('pipeline', Path(__file__).resolve().parents[1] / 'pipeline.py')
pipeline = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(pipeline)


class PipelineTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.artifact = pipeline.generate()
        cls.data = cls.artifact['data']

    def test_sample_matches_notebook_saved_outputs(self):
        self.assertEqual([s['n'] for s in self.data['selection']], [27509, 13299, 10091, 9881])
        self.assertEqual(self.data['overview']['income_median'], 474)
        self.assertEqual(self.data['overview']['hours_median'], 3)
        self.assertEqual(self.data['overview']['zero_hours_n'], 118)
        self.assertEqual(self.data['overview']['zero_income_n'], 119)

    def test_cluster_model_matches_notebook_precision(self):
        model = self.data['model']
        slope = model['coefficients'][1]
        self.assertAlmostEqual(slope['estimate'], 61.3563899864, places=8)
        self.assertAlmostEqual(slope['se'], 3.74723524757, places=8)
        self.assertAlmostEqual(slope['ci_low'], 54.0050195833, places=8)
        self.assertAlmostEqual(slope['ci_high'], 68.7077603894, places=8)
        self.assertAlmostEqual(slope['p'] / 7.10867239e-55, 1, places=7)
        self.assertEqual(model['clusters'], 1286)
        self.assertEqual(model['households'], 6448)
        self.assertEqual(model['strata'], 150)
        self.assertAlmostEqual(model['ser'], 568.786655533, places=7)

    def test_sensitivity_and_heteroskedasticity(self):
        model = self.data['model']
        self.assertEqual(model['cook_flagged_n'], 376)
        self.assertEqual(model['sensitivity']['n'], 9505)
        self.assertAlmostEqual(model['sensitivity']['slope'], 49.76, places=2)
        self.assertAlmostEqual(model['heteroskedasticity_p'], .006, places=4)
        self.assertTrue(all(row['n'] >= 30 for row in model['residual_spread']))

    def test_all_distributions_conserve_observations_and_zeros(self):
        for key in ['income', 'hours', 'groups']:
            self.assertEqual(sum(g['n'] for g in self.data[key]), 9881)
        self.assertEqual([g['n'] for g in self.data['groups']], [1661, 4515, 2312, 1132, 261])
        self.assertEqual(self.data['hours'][0], {'hours': 0, 'n': 118})
        self.assertEqual(self.data['income'][0]['lower'], 0)
        self.assertIsNone(self.data['income'][-1]['upper'])
        self.assertEqual(sum(r['n'] for r in self.data['availability']), 13299)

    def test_no_person_identifiers_in_public_aggregate(self):
        encoded = json.dumps(self.artifact)
        for name in ['id_persona', 'id_hogar', 'id_vivienda', 'ingrl_original', 'conglomerado']:
            self.assertNotIn(name, encoded)
        # V2 añade rejillas de conteos y cuantiles, nunca filas individuales.
        self.assertLess(len(encoded), 160000)
        pipeline.validate_artifact(self.artifact)

    def test_invalid_denominators_and_nonfinite_values_rejected(self):
        broken = copy.deepcopy(self.artifact)
        broken['data']['hours'][0]['n'] += 1
        with self.assertRaisesRegex(ValueError, 'observaciones'):
            pipeline.validate_artifact(broken)
        broken = copy.deepcopy(self.artifact)
        broken['data']['overview']['income_mean'] = float('nan')
        with self.assertRaises(ValueError):
            pipeline.validate_artifact(broken)

    def test_missing_and_changed_source_block_publication(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            with self.assertRaisesRegex(ValueError, 'Falta'):
                pipeline.load_sources(root)
            (root / 'data_clean.parquet').write_text('fuente alterada')
            with self.assertRaisesRegex(ValueError, 'cambió'):
                pipeline.load_sources(root)

    def test_reproducibility_excluding_generation_timestamp(self):
        saved = json.loads((pipeline.ROOT / 'frontend/public/data/dashboard.json').read_text())
        saved['meta'].pop('generated_at')
        regenerated = copy.deepcopy(self.artifact)
        regenerated['meta'].pop('generated_at')
        self.assertEqual(saved, regenerated)


if __name__ == '__main__':
    unittest.main()
