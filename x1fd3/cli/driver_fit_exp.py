from x1fd3.base.p_w_curve import PWCurve
from x1fd3.base.levels import Levels
from x1fd3.base.fit_funcs import exp_fit
from x1fd3.base.exp_data import ExpData
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
        self.expdata = ExpData(self.input_files[3])

    def core(
        self
    ) -> None:
        self.params['jmax'] = max(self.expdata.energy.keys())
        self.out.print('=== Fit PEC to reproduce exp. data ===\n')
        # print initial guess
        self.out.print('Initial guess')
        levels = Levels('an', self.params)
        levels.print_with_expdata(self.out, self.expdata)
        self.pec.print_with_an(self.params, self.out)
        # fit
        self.params, message, success = exp_fit(self.params, self.pec, self.expdata)
        if success:
            self.out.print(f'\nPEC fit done: {message}')
        else:
            raise RuntimeError(f'\nPEC fit FAILED: {message}')
        # print final results
        self.out.print('Fit results')
        levels = Levels('an', self.params)
        levels.print_with_expdata(self.out, self.expdata)
        self.pec.print_with_an(self.params, self.out)
        self.out.print('\nFitted parameters\n')
        self.params.print_pec_params(self.out)
