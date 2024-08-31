import sys

from funcs import *

if len(sys.argv) < 3:
    exit(
    '''Usage: python level_cacl_pw_pec.py <1> <2>
    <1> = file with parameters for level calc | example: vr_level_calc_params.txt
    <2> = file with point-wise pec            | example: pw_pec.txt'''
    )

f_vr_par = sys.argv[1]
f_pw_pec = sys.argv[2]

# print input
print_input_file(f_vr_par)
print_input_file(f_pw_pec)

# read files
pec = PWcurve(f_pw_pec)
params = read_vr_calc_params(f_vr_par, 'ENERGY')

# calc and print vr levels
levels = vr_solver('pw', params, pec)
print_levels(levels)
