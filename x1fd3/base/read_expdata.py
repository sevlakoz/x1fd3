from typing import Dict
from configparser import ConfigParser

def read_expdata(
        fname: str
    ) -> Dict[int, Dict[int, float]]:
    '''
    read exp vib-rot levels
    '''
    input_parser = ConfigParser(delimiters=(' ', '\t'))
    input_parser.read(fname)

    # read levels
    expdata = {}
    n_levels = 0

    for j in input_parser.sections():
        tmp = {}
        for v, en in input_parser[j].items():
            tmp[int(v)] = float(en)
            n_levels += 1
        expdata[int(j)] = tmp

    # check
    if n_levels == 0:
        raise RuntimeError(f'No energy levels found in {fname}')

    return expdata
