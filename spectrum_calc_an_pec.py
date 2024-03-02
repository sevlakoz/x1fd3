import sys

from funcs import *

if len(sys.argv) < 4:
	exit('Usage: python spectrum_cacl_an_pec.py <file with parameters for spectrum calc|example: vr_spectrum_calc_params.txt> <file with fitted parameters|example: emo_params.txt> <file with point-wise dm|example: dm.txt>')

f_vr_par = sys.argv[1]
f_fit_par = sys.argv[2]
f_pw_dm = sys.argv[3]

# print input
print_input_file(f_vr_par)
print_input_file(f_fit_par)
print_input_file(f_pw_dm)

# read files
params = read_pec_pars(f_fit_par)
params = params | read_vr_calc_pars(f_vr_par, 'SPECTRUM')
rd, fd = read_pw_curve(f_pw_dm)

# calc and print vr levels
levels = vr_solver('an', params)
print('\n=== Energy levels ===')
for j in levels.keys():
	print(f'\nJ = {j}\n  v    Energy,cm-1        Bv,cm-1')
	for v, lev in levels[j].items():
		print(f'{v:3d}{lev.energy:15.5f}{lev.rot_const:15.8f}')

# calc and print integrals
matrix_elements = me_calc(params, levels, rd, fd)
print("\n=== Intergals <f(v'J')|d|f(v''J'')>,D ===\n")
print(f"v'' = {params['v1']}")
print(f"v'  = {params['v2']}\n")
for j2 in range(0, params['jmax'] + 1):
	print(f"J' = {j2}")
	print(f" J''   <f'|d|f''>,D")
	for j1 in range(0, params['jmax'] + 1):
		print(f"{j1:4d}{matrix_elements[j2][j1]:15.5e}")
	print()

