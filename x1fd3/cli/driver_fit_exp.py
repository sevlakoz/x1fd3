from x1fd3.base.p_w_curve import PWCurve
from x1fd3.base.levels import Levels
from x1fd3.base.print_funcs import print_pecs
from x1fd3.base.fit_funcs import exp_fit
from x1fd3.base.read_expdata import read_expdata
from .driver import Driver

class DriverFitExp(Driver):
    '''
    Driver for FitExp mode
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
            raise RuntimeError(f'\nPEC fit FAILED: {message}')
        # print final results
        print('Fit results')
        levels = Levels('an', self.params)
        levels.print_with_expdata(self.expdata)
        print_pecs(self.pec, self.params)
        print('\nFitted parameters\n')
        self.params.print_pec_params()
