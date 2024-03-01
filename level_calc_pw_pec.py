import sys

from funcs import *

if len(sys.argv) < 3:
	exit('Usage: python level_cacl_pw_pec.py <file with parameters level calc|example: vr_level_calc_params.txt> <file with point-wise pec|example: pec.txt>')

f_vr_par = sys.argv[1]
f_pw_pec = sys.argv[2]

# print input
print_input_file(f_vr_par)
print_input_file(f_pw_pec)

# read files
rp, up = read_pw_curve(f_pw_pec)
params = read_vr_calc_pars(f_vr_par, 'ENERGY')

# calc and print vr levels
levels = vr_solver('pw', params, rp, up)
print('\n=== Energy levels ===')
for j in levels.keys():
	print(f'\nJ = {j}\n  v    Energy,cm-1        Bv,cm-1')
	for v, lev in levels[j].items():
		print(f'{v:3d}{lev.energy:15.5f}{lev.rot_const:15.8f}')
