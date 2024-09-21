from x1fd3.base.p_w_curve import PWCurve
from x1fd3.base.fit import Fit
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
        self.out.print('=== Fit PEC to reproduce exp. data ===\n')
        # jmax from exp data
        self.params['jmax'] = max(self.expdata.energy.keys())
        # init obj for fit
        fit = Fit(self.pec, self.params, self.expdata)
        # fit
        fit.fit_n_print(self.out)
