from math import factorial
import numpy as np
import numpy.typing as npt

from .parameters import Parameters

Float64Array = npt.NDArray[np.float64]

class AnPec:
    '''
    class for analytic pec functions
    '''
    def __init__(
        self,
        params:Parameters
    ) -> None:
        '''
        init params
        '''
        self.params = params

    def calc(
        self,
        r_inp:Float64Array,
    ) -> Float64Array:
        '''
        calculate pec vals for grid of Rs
        '''
        p = self.params
        s = 0.

        if p['te'] is not None and p['td'] is not None:
            raise RuntimeError('Both Te and Td given')

        if p['te'] is not None:
            s = p['te']

        if p['td'] is not None:
            s = p['td'] - p['de']

        match p['ptype']:
            case 'EMO':
                return self._emo(r_inp) + s
            case 'MLR':
                return self._mlr(r_inp) + s
            case 'DELR':
                return self._delr(r_inp) + s
            case _:
                raise RuntimeError(f"{p['ptype']} not implemented")


    def _emo(
        self,
        r_inp:Float64Array,
    ) -> Float64Array:
        '''
        calculate EMO value for given r point and params
        '''
        p = self.params

        yq = self._y(r_inp, p['q'], p['rref'])

        beta_pol = self._beta(yq)

        val:Float64Array = p['de'] * (1 - np.exp(- beta_pol * (r_inp - p['re'])))**2

        return val

    def _mlr(
        self,
        r_inp:Float64Array,
    ) -> Float64Array:
        '''
        calculate MLR value for given r point and params
        see https://doi.org/10.1063%2F1.3264688 for details
        '''
        p = self.params

        yq = self._y(r_inp, p['q'], p['rref'])
        yp = self._y(r_inp, p['p'], p['rref'])
        yp_eq = self._y(r_inp, p['p'], p['re'])

        ulr_re = self._lr(np.array([p['re']]))[0]
        ulr = self._lr(r_inp)

        binf = np.log(2 * p['de'] / ulr_re)
        beta_pol = self._beta(yq)
        beta_pol *= (1 - yp)
        beta_pol += binf * yp

        val:Float64Array = p['de'] * (1 - ulr / ulr_re * np.exp(- beta_pol * yp_eq))**2

        return val

    def _delr(
        self,
        r_inp:Float64Array
    ) -> Float64Array:
        '''
        calculate DELR value for given r point and params
        see https://doi.org/10.1063/1.1607313 for details
        '''
        p = self.params

        yq = self._y(r_inp, p['q'], p['rref'])
        yq_re = self._y(np.array([p['re']]), p['q'], p['rref'])

        beta_pol = self._beta(yq)
        beta_pol_re = self._beta(yq_re)[0]

        ulr = self._lr(r_inp)
        ulr_re = self._lr(np.array([p['re']]))[0]

        der_ulr_re = self._lr(np.array([p['re']]), 1)[0]

        a = p['de'] - ulr_re - der_ulr_re / beta_pol_re
        b = p['de'] - ulr_re + a

        val:Float64Array = p['de'] - ulr + a * np.exp(- 2 * beta_pol * (r_inp - p['re'])) \
                                          - b * np.exp(- beta_pol * (r_inp - p['re']))

        return val

    def _y(
        self,
        r_inp:Float64Array,
        q:int,
        rref:float
    ) -> Float64Array:
        '''
        calculate y function  value for given r points and params
        '''
        val:Float64Array = (r_inp**q - rref**q) / (r_inp**q + rref**q)
        return val

    def _beta(
        self,
        y_vals:Float64Array
    )-> Float64Array:
        '''
        calculate beta function value for given r point and params
        '''
        p = self.params

        val:Float64Array = np.zeros(len(y_vals))
        for n, b in enumerate(p['beta']):
            val += b * y_vals**n

        return val

    def _lr(
        self,
        r_inp:Float64Array,
        der_order:int=0
    ) -> Float64Array:
        '''
        calculate long-range value for given r point and params
        '''
        p = self.params

        val:Float64Array = np.zeros(len(r_inp))

        if der_order == 0:
            for n, cn in zip(p['cnpow'], p['cnval']):
                val += self._dampf(r_inp, n) * cn * r_inp**-n
        elif der_order == 1:
            for n, cn in zip(p['cnpow'], p['cnval']):
                val -= self._dampf(r_inp, n) * n * cn * r_inp**(- n - 1)
                val += self._dampf(r_inp, n, 1) * cn * r_inp**-n
        else:
            raise RuntimeError(f"order {der_order} not implemented")

        return val

    def _dampf(
        self,
        r_inp:Float64Array,
        n:int,
        der_order:int=0
    ) -> Float64Array:
        '''
        see https://doi.org/10.1080/00268976.2010.527304 for details
        params['dampf'] options:
        * 'ds'   - Douketis et al.
        * 'tt'   - Tang-Toennies
        * 'none' - disable damping
        s = 1/2 for 'ds' is not included
        '''
        btt = {
            2: 3.47,
            1: 3.13,
            0: 2.78,
           -1: 2.44,
           -2: 2.1
        }

        bds = {
            2: 4.99,
            1: 4.53,
            0: 3.95,
           -1: 3.3,
           -2: 2.5
        }

        cds = {
            2: 0.34,
            1: 0.36,
            0: 0.39,
           -1: 0.423,
           -2: 0.468
        }

        p = self.params
        s = p['s']
        rho = p['rho']

        val:Float64Array = np.zeros(len(r_inp))

        if der_order == 0:
            match p['dampf']:
                case 'tt':
                    ex = np.exp(- btt[s] * rho * r_inp)
                    sm = np.ones(len(r_inp))
                    for k in range(1, n + s):
                        sm += (btt[s] * rho * r_inp)**k / factorial(k)
                    val = 1 - ex * sm
                    return val
                case 'ds':
                    ex = np.exp(- bds[s] * rho * r_inp / n
                                - cds[s] * (rho * r_inp)**2 / n**0.5)
                    val = (1 - ex)**(n + s)
                    return val
                case 'none':
                    return np.ones(len(r_inp))
                case _:
                    raise RuntimeError(f"{p['dampf']} not implemented")
        elif der_order == 1:
            match p['dampf']:
                case 'tt':
                    ex = np.exp(- btt[s] * rho * r_inp)
                    sm = np.ones(len(r_inp))
                    dsm = np.zeros(len(r_inp))
                    for k in range(1, n + s):
                        sm += (btt[s] * rho * r_inp)**k / factorial(k)
                        dsm += k * btt[s] * rho *(btt[s] * rho * r_inp)**(k - 1) / factorial(k)
                    val = btt[s] * rho * ex * sm - dsm * ex
                    return val
                case 'ds':
                    ex = np.exp(- bds[s] * rho * r_inp / n
                                - cds[s] * (rho * r_inp)**2 / n**0.5)
                    val = (n + s) * (1 - ex)**(n + s - 1) * ex \
                           * (bds[s] * rho / n + 2 * cds[s] * rho**2 * r_inp / n**0.5)
                    return val
                case 'none':
                    return np.zeros(len(r_inp))
                case _:
                    raise RuntimeError(f"{p['dampf']} not implemented")
        else:
            raise RuntimeError(f"order {der_order} not implemented")
