import unittest
import numpy as np

from x1fd3.base import Parameters, \
                       PWCurve, \
                       AnPec, \
                       Levels, \
                       ExpData, \
                       MatrixElements, \
                       Fit


class TestBase(unittest.TestCase):

    def setUp(
        self
    ) -> None:

        pass


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

        self.assertAlmostEqual(
            expdata.energy[3][9],
            23828.05726,
            delta=1e-5
        )

    def test_05_levels(
        self
    ) -> None:

        params = Parameters()
        params.read_vr_calc_params('input/params_levels.txt', 'ENERGY')
        params['jmax'] = 1

        pec = PWCurve('input/pw_pec.txt')

        levels = Levels(params, pec, ExpData())

        self.assertAlmostEqual(
            levels.energy[0][0],
            1416.86703,
            delta=1e-5
        )

        self.assertAlmostEqual(
            levels.energy[1][0],
            1437.65647,
            delta=1e-5
        )

        expdata = ExpData('input/exp_levels.txt')

        params.read_pec_params('input/fitted_emo.txt')

        levels = Levels(params, PWCurve(), expdata)

        self.assertAlmostEqual(
            levels.energy[0][0],
            1473.01005,
            delta=1e-5
        )

        self.assertAlmostEqual(
            levels.energy[3][0],
            1597.70224,
            delta=1e-5
        )


    def test_06_matrix_elements(
        self
    ) -> None:

        params = Parameters()
        params.read_vr_calc_params('input/params_spectrum.txt', 'SPECTRUM')
        params['jmax'] = 1

        pec = PWCurve('input/pw_pec.txt')
        dm = PWCurve('input/pw_dm.txt')

        levels = Levels(params, pec, ExpData())

        melems = MatrixElements(params, levels, dm)

        self.assertAlmostEqual(
            melems.freq[0][1],
            2859.64817,
            delta=1e-5
        )

        self.assertAlmostEqual(
            melems.matrix_elements[0][1],
            0.071644,
            delta=1e-6
        )


    def test_07_fit(
        self
    ) -> None:

        params = Parameters()
        params.read_vr_calc_params('input/params_fit.txt', 'FIT')
        params.read_pec_params('input/fitted_emo.txt')
        pec = PWCurve('input/pw_pec.txt')
        expdata = ExpData('input/exp_levels.txt')

        fit = Fit(params, pec, expdata)
        fit.fit()

        self.assertAlmostEqual(
            fit.params['re'],
            1.27,
            delta=0.01
        )

if __name__ == '__main__':
    unittest.main(verbosity=2)
