import sys

from funcs import *

if len(sys.argv) < 3:
	exit('Usage: python pw_pec_approx.py <file with point-wise pec> <file with initial parameters>')

f_pw_pec = sys.argv[1]
f_init_par = sys.argv[2]

# print input 
print_input_file(f_pw_pec)
print_input_file(f_init_par)

# read files
rp, up = read_pw_curve(f_pw_pec)
params = read_pec_pars(f_init_par)

# print initial guess
print('=== Point-wise PEC approximation ===\n')
print('Initial guess\n')
print_pecs(rp, up, params)

# fit
params, message, success = pec_fit(rp, up, params)
if success:
	print(f'\nPoint-wise PEC approximation done: {message}')
else:
	exit(f'\nPoint-wise PEC approximation FAILED: {message}')

# final approximation
print('\nFitted PEC\n')
print_pecs(rp, up, params)
print('\nFitted parameters\n')
print_params(params)
print('\n=== End of point-wise PEC approximation ===\n')

