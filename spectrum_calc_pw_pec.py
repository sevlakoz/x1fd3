import sys

from funcs import *

if len(sys.argv) < 4:
	exit('Usage: python spectrum_cacl_pw_pec.py <file with parameters for spectrum calc|example: vr_spectrum_calc_params.txt> <file with point-wise pec|example: pec.txt> <file with point-wise dm|example: dm.txt>')

f_vr_par = sys.argv[1]
f_pw_pec = sys.argv[2]
f_pw_dm = sys.argv[3]

# print input
print_input_file(f_vr_par)
print_input_file(f_pw_pec)
print_input_file(f_pw_dm)

# read files
rp, up = read_pw_curve(f_pw_pec)
rd, fd = read_pw_curve(f_pw_dm)
params = read_vr_calc_pars(f_vr_par, 'SPECTRUM')

# calc and print vr levels
levels = vr_solver('pw', params, rp, up)
print_levels(levels)

# calc and print integrals
frequencies, matrix_elements = me_calc(params, levels, rd, fd)
print_matrix_elements(params, frequencies, matrix_elements)

