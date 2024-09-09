import sys
import abc
from typing import List, Dict, Tuple

from base.p_w_curve import PWCurve
from base.parameters import Parameters
from base.levels import Levels
from base.matrix_elements import MatrixElements
from base.print_funcs import print_input_file, print_pecs
from base.fit_funcs import pec_fit, exp_fit
from base.read_expdata import read_expdata

class Driver(abc.ABC):
    '''
    base abs class for driver, 
    contains data for input check and empty vars
    '''
    def __init__(
        self,
        input_files: list
    ):
        self.input_files: List[str] = input_files
        self.mode:str = type(self).__name__.replace('Driver_', '')
        self.input_error_message: Dict[str, Tuple[int, str]] = {
            'pw_pec_approx': (
                2,
                'Usage: python pw_pec_approx.py <1> <2>\n' + 
                '       <1> = file with point-wise pec     | example: pw_pec.txt\n' +
                '       <2> = file with initial parameters | example: init_emo_params.txt'
            ),
            'level_calc_pw_pec': (
                2,
                'Usage: python level_cacl_pw_pec.py <1> <2>\n' +
                '       <1> = file with parameters for level calc | example: vr_level_calc_params.txt\n' +
                '       <2> = file with point-wise pec            | example: pw_pec.txt'
            ),
            'level_calc_an_pec': (
                2,
                'Usage: python level_cacl_an_pec.py <1> <2>\n' +
                '       <1> = file with parameters for level calc | example: vr_level_calc_params.txt\n' +
                '       <2> = file with fitted parameters         | example: fitted_emo_params.txt'
            ),
            'spectrum_calc_pw_pec': (
                3,
                'Usage: python spectrum_cacl_pw_pec.py <1> <2> <3>\n' +
                '       <1> = file with parameters for spectrum calc | example: vr_spectrum_calc_params.txt\n' +
                '       <2> = file with point-wise pec               | example: pw_pec.txt\n' +
                '       <3> = file with point-wise dm                | example: pw_dm.txt'
            ),
            'spectrum_calc_an_pec': (
                3,
                'Usage: python spectrum_cacl_an_pec.py <1> <2> <3>\n' +
                '       <1> = file with parameters for spectrum calc | example: vr_spectrum_calc_params.txt\n' +
                '       <2> = file with fitted parameters            | example: fitted_emo_params.txt\n' +
                '       <3> = file with point-wise dm                | example: pw_dm.txt'
            ),
            'fit_pec_to_exp_levels': (
                4,
                'Usage: python fit_pec_to_exp_levels.py <1> <2> <3> <4>\n' +
                '       <1> = file with parameters for level calc | example: vr_fit_params.txt\n' +
                '       <2> = file with pre-fitted parameters     | example: fitted_emo_params.txt\n' +
                '       <3> = file with point-wise pec            | example: pw_pec.txt\n' +
                '       <4> = file with exp. vib.-rot. levels     | example: levels.txt'
            )
        }

        self.pec = PWCurve()
        self.dm = PWCurve()
        self.params = Parameters()
        self.expdata: Dict[int, Dict[int, float]] = {}

    def input_check(
        self
    ) -> None:
        '''
        check count of input files
        print error message if not enough 
        '''
        nf, mes = self.input_error_message[self.mode]
        if len(self.input_files) < nf:
            sys.exit(mes)

    def print_input_files(
        self
    ) -> None:
        '''
        print input files one by one
        '''
        for fname in self.input_files:
            print_input_file(fname)

    @abc.abstractmethod
    def read_files(
        self
    ) -> None:
        '''
        read files, store to vars, no pattern at all
        '''

    @abc.abstractmethod
    def core(
        self
    ) -> None:
        '''
        run calc & print stuff, no pattern at all
        '''

    def run(
        self
    ) -> None:
        '''
        run all task
        '''
        self.input_check()
        self.print_input_files()
        self.read_files()
        self.core()

class Driver_pw_pec_approx(Driver):
    '''
    Driver for pw_pec_approx mode
    '''
    def read_files(
        self
    ) -> None:
        self.pec = PWCurve(self.input_files[0])
        self.params.read_pec_params(self.input_files[1])

    def core(
        self
    ) -> None:
        # print initial guess
        print('=== Point-wise PEC approximation ===\n')
        print('Initial guess\n')
        print_pecs(self.pec, self.params)
        # fit
        self.params, message, success = pec_fit(self.pec, self.params)
        if success:
            print(f'\nPoint-wise PEC approximation done: {message}')
        else:
            sys.exit(f'\nPoint-wise PEC approximation FAILED: {message}')
        # final approximation
        print('\nFitted PEC\n')
        print_pecs(self.pec, self.params)
        print('\nFitted parameters\n')
        self.params.print_pec_params()

class Driver_level_calc_pw_pec(Driver):
    '''
    Driver for level_calc_pw_pec mode
    '''
    def read_files(
        self
    ) -> None:
        self.params.read_vr_calc_params(self.input_files[0], 'ENERGY')
        self.pec = PWCurve(self.input_files[1])

    def core(
        self
    ) -> None:
        # calc and print vr levels
        levels = Levels('pw', self.params, self.pec)
        levels.print()

class Driver_level_calc_an_pec(Driver):
    '''
    Driver for level_calc_pw_pec mode
    '''
    def read_files(
        self
    ) -> None:
        self.params.read_vr_calc_params(self.input_files[0], 'ENERGY')
        self.params.read_pec_params(self.input_files[1])

    def core(
        self
    ) -> None:
        # calc and print vr levels
        levels = Levels('an', self.params)
        levels.print()

class Driver_spectrum_calc_pw_pec(Driver):
    '''
    Driver for spectrum_calc_pw_pec mode
    '''
    def read_files(
        self
    ) -> None:
        self.params.read_vr_calc_params(self.input_files[0], 'SPECTRUM')
        self.pec = PWCurve(self.input_files[1])
        self.dm = PWCurve(self.input_files[2])

    def core(
        self
    ) -> None:
        # calc vr levels
        levels = Levels('pw', self.params, self.pec)
        # calc and print integrals
        matrix_elements = MatrixElements(self.params, levels, self.dm)
        matrix_elements.print()

class Driver_spectrum_calc_an_pec(Driver):
    '''
    Driver for spectrum_calc_an_pec mode
    '''
    def read_files(
        self
    ) -> None:
        self.params.read_vr_calc_params(self.input_files[0], 'SPECTRUM')
        self.params.read_pec_params(self.input_files[1])
        self.dm = PWCurve(self.input_files[2])

    def core(
        self
    ) -> None:
        # calc vr levels
        levels = Levels('an', self.params)
        # calc and print integrals
        matrix_elements = MatrixElements(self.params, levels, self.dm)
        matrix_elements.print()

class Driver_fit_pec_to_exp_levels(Driver):
    '''
    Driver for fit_pec_to_exp_levels mode
    '''
    def read_files(
        self
    ) -> None:
        self.params.read_vr_calc_params(self.input_files[0], 'FIT')
        self.params.read_pec_params(self.input_files[1])
        self.pec = PWCurve(self.input_files[2])
        self.expdata = read_expdata(self.input_files[3])

    def core(
        self
    ) -> None:
        self.params['jmax'] = max(self.expdata.keys())
        print('=== Fit PEC to reproduce exp. data ===\n')
        # print initial guess
        print('Initial guess')
        levels = Levels('an', self.params)
        levels.print_with_expdata(self.expdata)
        print_pecs(self.pec, self.params)
        # fit
        self.params, message, success = exp_fit(self.params, self.pec, self.expdata)
        if success:
            print(f'\nPEC fit done: {message}')
        else:
            sys.exit(f'\nPEC fit FAILED: {message}')
        # print final results
        print('Fit results')
        levels = Levels('an', self.params)
        levels.print_with_expdata(self.expdata)
        print_pecs(self.pec, self.params)
        print('\nFitted parameters\n')
        self.params.print_pec_params()
