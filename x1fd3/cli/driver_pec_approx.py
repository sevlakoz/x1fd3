from x1fd3.base.p_w_curve import PWCurve
from x1fd3.base.print_funcs import print_pecs
from x1fd3.base.fit_funcs import pec_fit
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
        # print initial guess
        self.out.print('=== Point-wise PEC approximation ===\n')
        self.out.print('Initial guess\n')
        print_pecs(self.out, self.pec, self.params)
        # fit
        self.params, message, success = pec_fit(self.pec, self.params)
        if success:
            self.out.print(f'\nPoint-wise PEC approximation done: {message}')
        else:
            raise RuntimeError(f'\nPoint-wise PEC approximation FAILED: {message}')
        # final approximation
        self.out.print('\nFitted PEC\n')
        print_pecs(self.out, self.pec, self.params)
        self.out.print('\nFitted parameters\n')
        self.params.print_pec_params(self.out)
