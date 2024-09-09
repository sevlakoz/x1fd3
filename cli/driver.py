import sys
import abc
from typing import List, Dict, Tuple

from base.p_w_curve import PWCurve
from base.parameters import Parameters
from base.print_funcs import print_input_file

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
        self.mode:str = type(self).__name__.replace('Driver', '')
        self.input_error_message: Dict[str, Tuple[int, str]] = {
            'PecApprox': (
                2,
                'Usage: python pw_pec_approx.py <1> <2>\n' + 
                '       <1> = file with point-wise pec     | example: pw_pec.txt\n' +
                '       <2> = file with initial parameters | example: init_emo_params.txt'
            ),
            'LevelsPw': (
                2,
                'Usage: python level_cacl_pw_pec.py <1> <2>\n' +
                '       <1> = file with parameters for level calc | example: vr_level_calc_params.txt\n' +
                '       <2> = file with point-wise pec            | example: pw_pec.txt'
            ),
            'LevelAn': (
                2,
                'Usage: python level_cacl_an_pec.py <1> <2>\n' +
                '       <1> = file with parameters for level calc | example: vr_level_calc_params.txt\n' +
                '       <2> = file with fitted parameters         | example: fitted_emo_params.txt'
            ),
            'SpectrumPW': (
                3,
                'Usage: python spectrum_cacl_pw_pec.py <1> <2> <3>\n' +
                '       <1> = file with parameters for spectrum calc | example: vr_spectrum_calc_params.txt\n' +
                '       <2> = file with point-wise pec               | example: pw_pec.txt\n' +
                '       <3> = file with point-wise dm                | example: pw_dm.txt'
            ),
            'SpectrumAn': (
                3,
                'Usage: python spectrum_cacl_an_pec.py <1> <2> <3>\n' +
                '       <1> = file with parameters for spectrum calc | example: vr_spectrum_calc_params.txt\n' +
                '       <2> = file with fitted parameters            | example: fitted_emo_params.txt\n' +
                '       <3> = file with point-wise dm                | example: pw_dm.txt'
            ),
            'FitExp': (
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
