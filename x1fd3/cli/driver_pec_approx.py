from x1fd3.base.p_w_curve import PWCurve
from x1fd3.base.fit import Fit
from .driver import Driver

class DriverPecApprox(Driver):
    '''
    Driver for PecApprox mode
    '''
    def read_files(
        self
    ) -> None:
        self.pec = PWCurve(self.input_files[0])
        self.params.read_pec_params(self.input_files[1])

    def core(
        self
    ) -> None:
        self.out.print('=== Point-wise PEC approximation ===\n')
        # fit and print
        Fit(self.pec, self.params).fit_n_print(self.out)
