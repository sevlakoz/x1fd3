from x1fd3.base import PWCurve, \
                       Fit, \
                       ExpData
from .driver import Driver

class DriverPecApprox(Driver):
    '''
    Driver for PecApprox mode
    '''
    def read_files(
        self
    ) -> None:
        self.params.read_pec_params(self.input_files[0])
        self.pec = PWCurve(self.input_files[1])

    def core(
        self
    ) -> None:
        self.out.print('=== Point-wise PEC approximation ===\n')
        # fit and print
        fit = Fit(self.params, self.pec, ExpData())
        fit.print_state('Initial', self.out)
        mes = fit.fit()
        self.out.print('\n' + mes + '\n')
        fit.print_state('Fitted', self.out)
