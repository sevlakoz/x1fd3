from base import emo, Parameters
import numpy as np

r = np.arange(2.0, 10.1, 0.1)

params = Parameters()

params['de'] = 10000.
params['re'] = 3.
params['rref'] = 4.
params['q'] = 2
params['beta'] = [1., 0.1, 0.01]

res = emo(r, params)

for x, y in zip(r, res):
    print(x, y)