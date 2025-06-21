import unittest
import numpy as np

from x1fd3.base import Parameters, \
                       PWCurve, \
                       AnPec, \
                       Levels, \
                       ExpData
                       #Fit
                       #


class TestBase(unittest.TestCase):

#    def setUp(
#        self
#    ) -> None:
#
#        pass


    def test_01_parameters(
        self
    ) -> None:

        params_vr_files = {
            'FIT': 'params_fit.txt',
            'ENERGY': 'params_levels.txt',
            'SPECTRUM': 'params_spectrum.txt'
        }

        for rtype, fname in params_vr_files.items():
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

        params_emo_files = [
            'init_emo.txt',
            'fitted_emo.txt'
        ]

        for fname in params_emo_files:
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


    def test_02_p_w_curve(
        self
    ) -> None:

        pw_data_files = [
            'pw_pec.txt',
            'pw_dm.txt'
        ]

        ref = [38.00497, 1.14716]

        for fname in pw_data_files:
            pec = PWCurve(f'input/{fname}')
            self.assertAlmostEqual(
                pec.spline(np.array([1.25]))[0],
                ref.pop(0),
                delta=1e-5
            )


    def test_03_an_pec(
        self
    ) -> None:

        params_emo_files = [
            'init_emo.txt',
            'fitted_emo.txt'
        ]

        ref = [15.20151, 98.84192]

        for fname in params_emo_files:
            params = Parameters()
            params.read_pec_params(f'input/{fname}')
            pec = AnPec(params)
            self.assertAlmostEqual(
                pec.calc(np.array([1.25]))[0],
                ref.pop(0),
                delta=1e-5
            )


    def test_04_expdata(
        self
    ) -> None:

        expdata = ExpData('input/exp_levels.txt')

        self.assertAlmostEqual(
            expdata.energy[0][0],
            1483.88056,
            delta=1e-5
        )

    def test_05_levels(
        self
    ):

        params = Parameters()
        params.read_vr_calc_params('input/params_levels.txt', 'ENERGY')
        params['jmax'] = 0

        pec = PWCurve('input/pw_pec.txt')

        levels = Levels(params, pec, ExpData())
        self.assertAlmostEqual(
            levels.energy[0][0],
            1416.86703,
            delta=1e-5
        )

        expdata = ExpData('input/exp_levels.txt')

        params.read_pec_params('input/fitted_emo.txt')
        levels = Levels(params, PWCurve(), expdata)
        self.assertAlmostEqual(
            levels.energy[3][0],
            1597.70224,
            delta=1e-5
        )



if __name__ == '__main__':
    unittest.main(verbosity=2)
