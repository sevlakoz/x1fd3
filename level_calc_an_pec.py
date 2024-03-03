import sys

from funcs import *

if len(sys.argv) < 3:
	exit('Usage: python level_cacl_an_pec.py <file with parameters for level calc|example: vr_level_calc_params.txt> <file with fitted parameters|example: emo_params.txt>')

f_vr_par = sys.argv[1]
f_fit_par = sys.argv[2]

# print input
print_input_file(f_vr_par)
print_input_file(f_fit_par)

# read files
params = read_pec_pars(f_fit_par)
params = params | read_vr_calc_pars(f_vr_par, 'ENERGY')

# calc and print vr levels
levels = vr_solver('an', params)
print_levels(levels)
