import numpy as np
from scipy.optimize import least_squares      # type: ignore

from .p_w_curve import PWCurve
from .parameters import Parameters
from .exp_data import ExpData
from .levels import Levels
from .an_pec import AnPec
from .logger import Logger

class Fit:
    '''
    least square fit 
    a)
    b) 
    '''
    def __init__(
        self,
        pec: PWCurve,
        params: Parameters,
        expdata: ExpData = ExpData()
    ) -> None:
        '''
        set input data, empty exp lelels list by default
        '''
        self.params = params
        self.pec = pec
        self.expdata = expdata


    def fit_n_print(
        self,
        out: Logger
    ) -> None:
        '''
        a) print initial guess
        b) perform least square fit
        c) print fit results
        '''
        # print initial guess
        out.print('Initial guess\n')
        self._print_pecs_n_levels(out)

        # init params
        guess = [self.params['de'], self.params['re']]
        guess.extend(self.params['beta'])

        # scipy least squares
        res_1 = least_squares(self._res, guess)
        if res_1.success:
            out.print(f'\nPEC fit done: {res_1.message}\n')
        else:
            raise RuntimeError(f'\nfit FAILED: {res_1.message}')

        # fitted params
        self.params['de'] = res_1.x[0]
        self.params['re'] = res_1.x[1]
        self.params['beta'] = np.array(list(res_1.x[2:]))

        # print final
        out.print('Fit results\n')
        self._print_pecs_n_levels(out)
        out.print('\nFitted parameters\n')
        self.params.print_pec_params(out)

    def _res(
        self,
        guess: list[float]
    ) -> list[float]:
        '''
        residual for fit
        '''
        # fitted params
        tmp = Parameters()
        tmp.update(self.params)

        tmp['de'] = guess[0]
        tmp['re'] = guess[1]
        tmp['beta'] = guess[2:]

        # residual calc
        res:list[float] = []

        # exp levels
        if self.expdata.nlev > 0:
            levels = Levels(tmp, PWCurve(), self.expdata)
            for j, en_jv in self.expdata.energy.items():
                for v, en_v in en_jv.items():
                    res.append((levels.energy[j][v] - en_v) / 0.1)

        # pec
        pec_an = AnPec(tmp).calc(self.pec.rval)
        res.extend((self.pec.cval - pec_an) / self.pec.eval)

        return res

    def _print_pecs_n_levels(
        self,
        out: Logger
    ) -> None:
        '''
        print pec and exp levels if provided
        '''
        if self.expdata.nlev > 0:
            levels = Levels(self.params, PWCurve(), self.expdata)
            levels.print_with_expdata(out, self.expdata)
        self.pec.print_with_an(self.params, out)
