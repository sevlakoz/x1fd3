'''
analytic pec functions
'''
import numpy as np
import numpy.typing as npt

from .parameters import Parameters

def emo(
        r_inp: npt.NDArray[np.float64],
        params: Parameters
    ) -> npt.NDArray[np.float64]:
    '''
    calculate EMO value for given r point and params
    '''
    yq = y(r_inp, params['q'], params['rref'])

    beta_pol = beta(r_inp, params['beta'], yq)

    val = params['de'] * (1 - np.exp(- beta_pol * (r_inp - params['re'])))**2

    return val

def mlr(
        r_inp: npt.NDArray[np.float64],
        params: Parameters
    ) -> npt.NDArray[np.float64]:
    '''
    calculate MLR value for given r point and params
    '''
    yq = y(r_inp, params['q'], params['rref'])
    yp = y(r_inp, params['p'], params['rref'])
    yp_eq = y(r_inp, params['p'], params['re'])

    ulr_re = float(lr(np.array([params['re']]), params)[0])
    ulr = lr(r_inp, params)

    binf = np.log(2 * params['de'] / ulr_re)
    beta_pol = beta(r_inp, params['beta'], yq)
    beta_pol *= (1 - yp)
    beta_pol += binf * yp

    val = params['de'] * (1 - ulr / ulr_re * np.exp(- beta_pol * yp_eq))**2

    return val

def delr(
        r_inp: npt.NDArray[np.float64],
        params: Parameters
    ) -> npt.NDArray[np.float64]:
    '''
    calculate DELR value for given r point and params
    '''
    yq = y(r_inp, params['q'], params['rref'])

    beta_pol = beta(r_inp, params['beta'], yq)
    beta_pol_re = float(beta(np.array([params['re']]), params['beta'], yq)[0])

    ulr = lr(r_inp, params)
    ulr_re = float(lr(np.array([params['re']]), params)[0])

    der_ulr_re = float(der_lr(np.array([params['re']]), params)[0])

    a = params['de'] - ulr_re - der_ulr_re / beta_pol_re
    b = params['de'] - ulr_re + a

    val = params['de'] - ulr + a * np.exp(- 2 * beta_pol * (r_inp - params['re'])) \
                             - b * np.exp(- beta_pol * (r_inp - params['re']))

    return val

def y(
        r_inp: npt.NDArray[np.float64],
        q: int,
        rref: float
    ) -> npt.NDArray[np.float64]:
    '''
    calculate y function  value for given r point and params
    '''
    return (r_inp**q - rref**q) / (r_inp**q + rref**q)

def beta(
        r_inp: npt.NDArray[np.float64],
        beta_coefs: list[float],
        y_vals: npt.NDArray[np.float64]
    )-> npt.NDArray[np.float64]:
    '''
    calculate beta function value for given r point and params
    '''
    val = np.zeros(len(r_inp))
    for n, b in enumerate(beta_coefs):
        val += b * y_vals**n

    return val

def lr(
        r_inp: npt.NDArray[np.float64],
        params: Parameters
    ) -> npt.NDArray[np.float64]:
    '''
    calculate long-range value for given r point and params
    '''
    val = np.zeros(len(r_inp))
    for n, cn in zip(params['cnpow'], params['cnval']):
        val += cn * r_inp**-n

    return val

def der_lr(
        r_inp: npt.NDArray[np.float64],
        params: Parameters
    ) -> npt.NDArray[np.float64]:
    '''
    calculate d(long-range)/dR value for given r point and params
    '''
    val = np.zeros(len(r_inp))
    for n, cn in zip(params['cnpow'], params['cnval']):
        val -= n * cn * r_inp**(- n - 1)

    return val
