from x1fd3.base import PWCurve, \
                       Fit, \
                       ExpData
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
        self.out.print('=== Fit PEC to reproduce exp. data ===\n')
        # fit
        fit = Fit(self.params, self.pec, self.expdata)
        fit.print_state('Initial', self.out)
        fit.fit(self.out)
        fit.print_state('Fitted', self.out)
