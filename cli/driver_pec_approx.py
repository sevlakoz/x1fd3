import sys

from base.p_w_curve import PWCurve
from base.print_funcs import print_pecs
from base.fit_funcs import pec_fit
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
