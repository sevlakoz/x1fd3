import numpy as np

from .parameters import Parameters

def emo(
        r_inp: np.ndarray,
        params: Parameters
    ) -> np.ndarray:
    '''
    calculate EMO value for given r point and params
    '''

    # EMO calc
    y = (r_inp**params['q'] - params['rref']**params['q']) / \
        (r_inp**params['q'] + params['rref']**params['q'])

    beta_pol = 0.
    for n, beta in enumerate(params['beta']):
        beta_pol += beta * y**n

    return params['de'] * (1 - np.exp(- beta_pol * (r_inp - params['re'])))**2   # type: ignore
