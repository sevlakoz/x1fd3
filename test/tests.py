import unittest

from x1fd3.base import Parameters
                       #PWCurve
                       #Fit
                       #ExpData


class TestOnlineInference(unittest.TestCase):

    def setUp(
        self
    ) -> None:
        self.params_vr_files = {
            'FIT': 'params_fit.txt',
            'ENERGY': 'params_levels.txt',
            'SPECTRUM': 'params_spectrum.txt'
        }

        self.params_emo_files = [
            'init_emo.txt',
            'fitted_emo.txt'
        ]


    def test_parameters(
        self
    ) -> None:
        for rtype, fname in self.params_vr_files.items():
            params = Parameters()
            params.read_vr_calc_params(f'input/{fname}', rtype)

            self.assertAlmostEqual(
                params['mass1'],
                1.007825,
                delta=1e-15
            )
            self.assertAlmostEqual(
                params['mass2'],
                34.968852,
                delta=1e-15
            )
            self.assertAlmostEqual(
                params['rmin'],
                0.7,
                delta=1e-15
            )
            self.assertAlmostEqual(
                params['rmax'],
                5.0,
                delta=1e-15
            )

            if rtype in ['ENERGY', 'SPECTRUM']:
                self.assertEqual(
                    params['jmax'],
                    10
                )

                if rtype == 'SPECTRUM':
                    self.assertEqual(
                        params['v1'],
                        0
                    )

                    self.assertEqual(
                        params['v2'],
                        1
                    )

        for fname in self.params_emo_files:
            params = Parameters()
            params.read_pec_params(f'input/{fname}')

            self.assertAlmostEqual(
                params['de'],
                37000.,
                delta=500
            )

            self.assertAlmostEqual(
                params['re'],
                1.27,
                delta=0.01
            )

            self.assertAlmostEqual(
                params['rref'],
                1.5,
                delta=1e-15
            )

            self.assertEqual(
                params['q'],
                3
            )

            self.assertEqual(
                len(params['beta']),
                5
            )


if __name__ == '__main__':
    unittest.main()
