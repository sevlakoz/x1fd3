import sys
from typing import Dict
import numpy as np

from .classPWcurve import PWcurve
from .classLevels import Levels
from .classParameters import Parameters

class MatrixElements:
    '''
    class for matrix elements
    '''
    def __init__(
        self,
        params: Parameters,
        levels: Levels,
        dm: PWcurve
    ) -> None:
        '''
        init = calculate matrix elements of given dipole function
        '''
        self.v1: int = params['v1']
        self.v2: int = params['v2']

        self.energy1: Dict[int, Dict[int, float]] = {}
        self.freq: Dict[int, Dict[int, float]] = {}
        self.matrix_elements: Dict[int, Dict[int, np.float64]] = {}

        # cubic spline to find DM values
        d_grid = dm.spline(levels.r_grid)

        # matrix elements calc
        for j2 in levels.energy.keys():
            self.energy1[j2] = {}
            self.freq[j2] = {}
            self.matrix_elements[j2] = {}
            for j1 in levels.energy.keys():
                self.energy1[j2][j1] = levels.energy[j1][self.v1]
                self.freq[j2][j1] = levels.energy[j2][self.v2] - levels.energy[j1][self.v1]
                self.matrix_elements[j2][j1] = np.sum(
                    levels.wavef_grid[j1][self.v1] *
                    levels.wavef_grid[j2][self.v2] *
                    d_grid
                )

    def print(
        self
    ) -> None:
        '''
        print calculated matrix elements in custom format
        '''
        print("\n=== Transition energies & Intergals <f(v',J')|d|f(v'',J'')>,D ===\n")
        print(f"v'' = {self.v1}")
        print(f"v'  = {self.v2}\n")

        for j2, me_j2j1 in self.matrix_elements.items():
            print(f"J' = {j2}")
            print(f'''{"J''":>4}{"freq,cm-1":>15}{"E'',cm-1":>15}{"<f'|d|f''>,D":>15}''')
            for j1, me in me_j2j1.items():
                en1 = self.energy1[j2][j1]
                frq  = self.freq[j2][j1]
                print(f"{j1:4d}{frq:15.5f}{en1:15.5f}{me:15.5e}")
            print()

    def _ht(
        self
    ) -> None:
        '''
        ht comp
        '''
        jm = max(self.matrix_elements.keys())

        jlist = []
        for j1 in range(jm, 0, -1):
            j2 = j1 - 1
            jlist.append((j2, j1))
        for j1 in range(jm):
            j2 = j1 + 1
            jlist.append((j2, j1))

        hdrs = ["Branch", "J'", "J''", "freq", "me", "Sa", "E''", "pop", "int", "Se", "A"]
        wds  = [ 6,        4,    4,     15,     15,   10,   15,    15,    15,    10,   15]
        fts  = ['',       'd',  'd',  '.5f',  '.5e','.5f','.5f', '.5e', '.5e', '.5f','.5e']

        for wd, hdr in zip(wds, hdrs):
            print(f'{hdr:>{wd}}', end = '')
        print()

        for j2, j1 in jlist:
            dj = j2 - j1
            if dj == 1:
                lbl = "R"
                sa = (j1 + 1) / (2 * j1 + 1)
                se =  j2      / (2 * j2 + 1)
            elif dj == -1:
                lbl = "P"
                sa = j1       / (2 * j1 + 1)
                se = (j2 + 1) / (2 * j2 + 1)
            else:
                sys.exit('ERROR: wrong dJ')

            en1 = self.energy1[j2][j1]
            frq  = self.freq[j2][j1]
            me = self.matrix_elements[j2][j1]

            pop = (2 * j1 + 1) * np.exp(-en1 / 0.695 / 298.0)
            a = 3.137e-7 * me**2 * se * frq**3
            inten = pop * me**2 * sa

            vals = [lbl, j2, j1, frq, me, sa, en1, pop, inten, se, a]
            for val, wd, ft in zip(vals, wds, fts):
                print(f'{val:{wd}{ft}}', end = '')
            print()
