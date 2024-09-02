import sys

from funcs import print_input_file, PWcurve, read_pec_params,\
                  print_pecs, pec_fit, print_pec_params

if len(sys.argv) < 3:
    sys.exit(
    '''Usage: python pw_pec_approx.py <1> <2>
    <1> = file with point-wise pec     | example: pw_pec.txt
    <2> = file with initial parameters | example: init_emo_params.txt'''
    )

f_pw_pec = sys.argv[1]
f_init_par = sys.argv[2]

# print input
print_input_file(f_pw_pec)
print_input_file(f_init_par)

# read files
pec = PWcurve(f_pw_pec)
params = read_pec_params(f_init_par)

# print initial guess
print('=== Point-wise PEC approximation ===\n')
print('Initial guess\n')
print_pecs(pec, params)

# fit
params, message, success = pec_fit(pec, params)
if success:
    print(f'\nPoint-wise PEC approximation done: {message}')
else:
    sys.exit(f'\nPoint-wise PEC approximation FAILED: {message}')

# final approximation
print('\nFitted PEC\n')
print_pecs(pec, params)
print('\nFitted parameters\n')
print_pec_params(params)

