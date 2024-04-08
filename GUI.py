import os

import sys

from funcs import *

import tkinter as tk
from tkinter import filedialog
from tkinter import ttk

#=======================================================================
#=======================================================================

def select_mode(mode):
	
	for widget in frame.winfo_children():
		widget.grid_forget()
	
	hdr_input_files.grid(
		row = 100, 
		column = 0,
		columnspan = 4
	)
	
	if mode.get() in [
		'pw_pec_approx',
		'lev_calc_pw',
		'sp_calc_pw',
		'fit_pec_to_exp'
	]:
			lbl_pw_pec.grid(
				row = 101, 
				column = 0
			)
			
			file_pw_pec.grid(
				row = 101, 
				column = 1
			)
			
			open_pw_pec.grid(
				row = 101, 
				column = 2
			)
	
	if mode.get() in [
		'lev_calc_pw',
		'lev_calc_an'
	]:
		
		lbl_lev_calc.grid(
			row = 102, 
			column = 0
		)
		
		file_lev_calc.grid(
			row = 102, 
			column = 1
		)
		
		open_lev_calc.grid(
			row = 102, 
			column = 2
		)
	
	if mode.get() in [
		'sp_calc_pw',
		'sp_calc_an'
	]:
		
		lbl_sp_calc.grid(
			row = 103, 
			column = 0
		)
		
		file_sp_calc.grid(
			row = 103, 
			column = 1
		)
		
		open_sp_calc.grid(
			row = 103, 
			column = 2
		)
	
	if mode.get() in [
		'fit_pec_to_exp'
	]:
		
		lbl_fit_calc.grid(
			row = 104, 
			column = 0
		)
		
		file_fit_calc.grid(
			row = 104, 
			column = 1
		)
		
		open_fit_calc.grid(
			row = 104, 
			column = 2
		)
	
	if mode.get() in [
		'pw_pec_approx'
	]:
		lbl_init_pars.grid(
			row = 105, 
			column = 0
		)
		
		file_init_pars.grid(
			row = 105, 
			column = 1
		)
		
		open_init_pars.grid(
			row = 105, 
			column = 2
		)
	
	if mode.get() in [
		'lev_calc_an',
		'sp_calc_an',
		'fit_pec_to_exp'
	]:
		lbl_fitted_pars.grid(
			row = 106, 
			column = 0
		)
		
		file_fitted_pars.grid(
			row = 106, 
			column = 1
		)
		
		open_fitted_pars.grid(
			row = 106, 
			column = 2
		)
	
	if mode.get() in [
		'sp_calc_pw',
		'sp_calc_an'
	]:
			lbl_pw_dip.grid(
				row = 107, 
				column = 0
			)
			
			file_pw_dip.grid(
				row = 107, 
				column = 1
			)
			
			open_pw_dip.grid(
				row = 107, 
				column = 2
			)
	
	if mode.get() in [
		'fit_pec_to_exp'
	]:
			lbl_exp.grid(
				row = 108, 
				column = 0
			)
			
			file_exp.grid(
				row = 108, 
				column = 1
			)
			
			open_exp.grid(
				row = 108, 
				column = 2
			)
	
	hdr_out.grid(
		row = 110, 
		column = 0,
		columnspan = 4
	)
	
	lbl_out.grid(
		row = 111, 
		column = 0
	)
	
	file_out.grid(
		row = 111, 
		column = 1
	)
	
	open_out.grid(
		row = 111, 
		column = 2
	)
	
	vscroll.grid(
		row = 112, 
		column = 3, 
		sticky = tk.N + tk.S
	)
	
	message_window.grid(
		row = 112, 
		column = 0, 
		columnspan = 3
	)
	
	run.grid(
		row = 113, 
		column = 0,
		columnspan = 4
	)
	
	frame.grid(
		row = 10, 
		column = 0,
		columnspan = 4
	)


#=======================================================================

def print_message(string, prnt = True):
	
	if prnt:
		print(string)
	
	message_window.configure(state = 'normal')
	message_window.insert('end', string)
	message_window.configure(state = 'disabled')

#=======================================================================

def select_file(obj):
	filetypes = (
		('text files', '*.txt'),
		('All files', '*.*')
	)

	fname = filedialog.askopenfilename(
		title = 'Open a file',
		filetypes = filetypes
	)
	
	if os.getcwd() == os.path.dirname(fname):
		fname = os.path.basename(fname)
	
	obj.delete(0, 'end')
	obj.insert(0, fname)


#=======================================================================

def run_calc(mode):
	
	fname = file_out.get()
	if fname:
		if os.path.isfile(fname) and os.path.getsize(fname) > 0:
			print_message(f'ERROR: non-empty out file "{fname}" already exists\n', False)
			return
	else:
		print_message('ERROR: out file not specified\n', False)
		return
	out = open(fname, 'w')
	
	sys.stdout = out
	
	#---
	
	if mode.get() == 'pw_pec_approx':
		
		f_pw_pec = file_pw_pec.get()
		f_init_par = file_init_pars.get()
		
		# print input
		try:
			print('* Point-wise PEC *')
			print_input_file(f_pw_pec)
			out.flush()
		except BaseException as ex:
			print_message(f'ERROR: failed to read input file with point-wise PEC: {str(ex)}\n')
			out.flush()
			return
		
		try:
			print('* Init EMO parameters *')
			print_input_file(f_init_par)
			out.flush()
		except BaseException as ex:
			print_message(f'ERROR: failed to read input file with initial EMO parameters: {str(ex)}\n')
			out.flush()
			return
		
		# read files
		try: 
			rp, up = read_pw_curve(f_pw_pec)
		except BaseException as ex:
			print_message(f'ERROR: failed to read point-wise PEC: {str(ex)}\n')
			out.flush()
			return
		
		try:
			params = read_pec_pars(f_init_par)
		except BaseException as ex:
			print_message(f'ERROR: failed to read initial EMO parameters: {str(ex)}\n')
			out.flush()
			return
		
		# print initial guess
		print('=== Point-wise PEC approximation ===\n')
		print('Initial guess\n')
		print_pecs(rp, up, params)
		out.flush()
		
		# fit
		try:
			params, message, success = pec_fit(rp, up, params)
			if success:
				print(f'\nPoint-wise PEC approximation done: {message}')
				out.flush()
			else:
				print_message(f'ERROR: point-wise PEC approximation FAILED: {message}\n')
				out.flush()
				return
		except BaseException as ex:
			print_message(f'ERROR: failed to run "pec_fit" function: {str(ex)}\n')
			out.flush()
			return
		
		# final approximation
		print('\nFitted PEC\n')
		print_pecs(rp, up, params)
		print('\nFitted parameters\n')
		print_params(params)
		out.flush()
	
	#---
	
	if mode.get() == 'lev_calc_pw':
		
		f_vr_par = file_lev_calc.get()
		f_pw_pec = file_pw_pec.get()
		
		# print input
		try:
			print('* Parameter for vib.-rot. levels calculation *')
			print_input_file(f_vr_par)
			out.flush()
		except BaseException as ex:
			print_message(f'ERROR: failed to read input file with parameter for vib.-rot. levels calculation: {str(ex)}\n')
			out.flush()
			return
		
		try:
			print('* Point-wise PEC *')
			print_input_file(f_pw_pec)
			out.flush()
		except BaseException as ex:
			print_message(f'ERROR: failed to read input file with point-wise PEC: {str(ex)}\n')
			out.flush()
			return
		
		# read files
		try: 
			rp, up = read_pw_curve(f_pw_pec)
		except BaseException as ex:
			print_message(f'ERROR: failed to read point-wise PEC: {str(ex)}\n')
			out.flush()
			return
		
		try:
			params = read_vr_calc_pars(f_vr_par, 'ENERGY')
		except BaseException as ex:
			print_message(f'ERROR: failed to read parameter for vib.-rot. levels calculation: {str(ex)}\n')
			out.flush()
			return
		
		# calc and print vr levels
		try:
			levels = vr_solver('pw', params, rp, up)
		except BaseException as ex:
			print_message(f'ERROR: failed to run "vr_solver" function: {str(ex)}\n')
			out.flush()
			return
		
		print_levels(levels)
		out.flush()
	
	#---
	
	if mode.get() == 'lev_calc_an':
		
		f_vr_par = file_lev_calc.get()
		f_fit_par = file_fitted_pars.get()
		
		# print input
		try:
			print('* Parameter for vib.-rot. levels calculation *')
			print_input_file(f_vr_par)
			out.flush()
		except BaseException as ex:
			print_message(f'ERROR: failed to read input file with parameter for vib.-rot. levels calculation: {str(ex)}\n')
			out.flush()
			return
		
		try:
			print('* Fitted EMO parameters *')
			print_input_file(f_fit_par)
			out.flush()
		except BaseException as ex:
			print_message(f'ERROR: failed to read input file with fitted EMO parameters: {str(ex)}\n')
			out.flush()
			return
		
		# read files
		try:
			params = read_vr_calc_pars(f_vr_par, 'ENERGY')
		except BaseException as ex:
			print_message(f'ERROR: failed to read parameter for vib.-rot. levels calculation: {str(ex)}\n')
			out.flush()
			return
		
		try:
			params = params | read_pec_pars(f_fit_par)
		except BaseException as ex:
			print_message(f'ERROR: failed to read fitted EMO parameters: {str(ex)}\n')
			out.flush()
			return
		
		
		# calc and print vr levels
		try:
			levels = vr_solver('an', params)
		except BaseException as ex:
			print_message(f'ERROR: failed to run "vr_solver" function: {str(ex)}\n')
			out.flush()
			return
		
		print_levels(levels)
		out.flush()
	
	#---
	
	if mode.get() == 'sp_calc_pw':
	
		f_vr_par = file_sp_calc.get()
		f_pw_pec = file_pw_pec.get()
		f_pw_dm = file_pw_dip.get()
		
		# print input
		try:
			print('* Parameters for vib.-rot. spectrum calculation *')
			print_input_file(f_vr_par)
			out.flush()
		except BaseException as ex:
			print_message(f'ERROR: failed to read input file with parameter for vib.-rot. spectrum calculation: {str(ex)}\n')
			out.flush()
			return
		
		try:
			print('* Point-wise PEC *')
			print_input_file(f_pw_pec)
			out.flush()
		except BaseException as ex:
			print_message(f'ERROR: failed to read input file with point-wise PEC: {str(ex)}\n')
			out.flush()
			return
		
		try:
			print('* Point-wise dipole moment *')
			print_input_file(f_pw_dm)
			out.flush()
		except BaseException as ex:
			print_message(f'ERROR: failed to read input file with point-wise dipole moment: {str(ex)}\n')
			out.flush()
			return
		
		# read files
		try: 
			rp, up = read_pw_curve(f_pw_pec)
		except BaseException as ex:
			print_message(f'ERROR: failed to read point-wise PEC: {str(ex)}\n')
			out.flush()
			return
		
		try: 
			rd, fd = read_pw_curve(f_pw_dm)
		except BaseException as ex:
			print_message(f'ERROR: failed to read point-wise dipole moment: {str(ex)}\n')
			out.flush()
			return
		
		try:
			params = read_vr_calc_pars(f_vr_par, 'SPECTRUM')
		except BaseException as ex:
			print_message(f'ERROR: failed to read parameter for vib.-rot. spectrum calculation: {str(ex)}\n')
			out.flush()
			return
		
		# calc vr levels
		try:
			levels = vr_solver('pw', params, rp, up)
		except BaseException as ex:
			print_message(f'ERROR: failed to run "vr_solver" function: {str(ex)}\n')
			out.flush()
			return
		
		# calc and print integrals
		try:
			matrix_elements = me_calc(params, levels, rd, fd)
		except BaseException as ex:
			print_message(f'ERROR: failed to run "matrix_elements" function: {str(ex)}\n')
			out.flush()
			return
		
		print_matrix_elements(params, levels, matrix_elements)
		out.flush()
	
	#---
	
	if mode.get() == 'sp_calc_an':
		
		f_vr_par = file_sp_calc.get()
		f_fit_par = file_fitted_pars.get()
		f_pw_dm = file_pw_dip.get()
		
		# print input
		try:
			print('* Parameters for vib.-rot. spectrum calculation *')
			print_input_file(f_vr_par)
			out.flush()
		except BaseException as ex:
			print_message(f'ERROR: failed to read input file with parameter for vib.-rot. spectrum calculation: {str(ex)}\n')
			out.flush()
			return
		
		try:
			print('* Fitted EMO parameters *')
			print_input_file(f_fit_par)
			out.flush()
		except BaseException as ex:
			print_message(f'ERROR: failed to read input file with fitted EMO parameters: {str(ex)}\n')
			out.flush()
			return
		
		try:
			print('* Point-wise dipole moment *')
			print_input_file(f_pw_dm)
			out.flush()
		except BaseException as ex:
			print_message(f'ERROR: failed to read input file with point-wise dipole moment: {str(ex)}\n')
			out.flush()
			return
		
		# read files
		try:
			params = read_vr_calc_pars(f_vr_par, 'SPECTRUM')
		except BaseException as ex:
			print_message(f'ERROR: failed to read parameter for vib.-rot. spectrum calculation: {str(ex)}\n')
			out.flush()
			return
		
		try:
			params = params | read_pec_pars(f_fit_par)
		except BaseException as ex:
			print_message(f'ERROR: failed to read fitted EMO parameters: {str(ex)}\n')
			out.flush()
			return
		
		try: 
			rd, fd = read_pw_curve(f_pw_dm)
		except BaseException as ex:
			print_message(f'ERROR: failed to read point-wise dipole moment: {str(ex)}\n')
			out.flush()
			return
		
		# calc vr levels
		try:
			levels = vr_solver('an', params)
		except BaseException as ex:
			print_message(f'ERROR: failed to run "vr_solver" function: {str(ex)}\n')
			out.flush()
			return
		
		# calc and print integrals
		try:
			matrix_elements = me_calc(params, levels, rd, fd)
		except BaseException as ex:
			print_message(f'ERROR: failed to run "matrix_elements" function: {str(ex)}\n')
			out.flush()
			return
		
		print_matrix_elements(params, levels, matrix_elements)
		out.flush()
	
	#---
	
	if mode.get() == 'fit_pec_to_exp':
		
		f_vr_par = file_fit_calc.get()
		f_fit_par = file_fitted_pars.get()
		f_pw_pec = file_pw_pec.get()
		f_epx_lev = file_exp.get()
		
		# print input
		try:
			print('* Parameters for PEC fit to exp. levels *')
			print_input_file(f_vr_par)
			out.flush()
		except BaseException as ex:
			print_message(f'ERROR: failed to read input file with parameter for PEC fit to exp. levels: {str(ex)}\n')
			out.flush()
			return
		
		try:
			print('* Fitted EMO parameters *')
			print_input_file(f_fit_par)
			out.flush()
		except BaseException as ex:
			print_message(f'ERROR: failed to read input file with fitted EMO parameters: {str(ex)}\n')
			out.flush()
			return
		
		try:
			print('* Point-wise PEC *')
			print_input_file(f_pw_pec)
			out.flush()
		except BaseException as ex:
			print_message(f'ERROR: failed to read input file with point-wise PEC: {str(ex)}\n')
			out.flush()
			return
		
		try:
			print('* Exp. levels *')
			print_input_file(f_epx_lev)
			out.flush()
		except BaseException as ex:
			print_message(f'ERROR: failed to read input file with exp. vib.-rot. levels: {str(ex)}\n')
			out.flush()
			return
		
		# read files
		try: 
			rp, up = read_pw_curve(f_pw_pec)
		except BaseException as ex:
			print_message(f'ERROR: failed to read point-wise PEC: {str(ex)}\n')
			out.flush()
			return
		
		try:
			params = read_vr_calc_pars(f_vr_par, 'FIT')
		except BaseException as ex:
			print_message(f'ERROR: failed to read parameter for PEC fit to exp. levels: {str(ex)}\n')
			out.flush()
			return
		
		try:
			params = params | read_pec_pars(f_fit_par)
		except BaseException as ex:
			print_message(f'ERROR: failed to read fitted EMO parameters: {str(ex)}\n')
			out.flush()
			return
		
		try:
			expdata = read_expdata(f_epx_lev)
		except BaseException as ex:
			print_message(f'ERROR: failed to read exp. vib.-rot. levels: {str(ex)}\n')
			out.flush()
			return
		
		params['jmax'] = max(expdata.keys())
		
		print('=== Fit PEC to reproduce exp. data ===\n')
		
		# print initial guess
		print('Initial guess')
		try:
			levels = vr_solver('an', params)
		except BaseException as ex:
			print_message(f'ERROR: failed to run "vr_solver" function: {str(ex)}\n')
			out.flush()
			return
		
		print_levels_n_expdata(params, levels, expdata)
		print_pecs(rp, up, params)
		out.flush()
		
		# fit
		try:
			params, message, success = exp_fit(params, rp, up, expdata)
			if success:
				print(f'\nPEC fit to exp. levels done: {message}')
				out.flush()
			else:
				print_message(f'ERROR: PEC fit to exp. levels FAILED: {message}')
				out.flush()
				return
		except BaseException as ex:
			print_message(f'ERROR: failed to run "exp_fit" function: {str(ex)}\n')
			out.flush()
			return
		
		# print final results
		print('\nFit results')
		try:
			levels = vr_solver('an', params)
		except BaseException as ex:
			print_message(f'ERROR: failed to run "vr_solver" function: {str(ex)}\n')
			out.flush()
			return
		print_levels_n_expdata(params, levels, expdata)
		print_pecs(rp, up, params)
		print('\nFitted parameters\n')
		print_params(params)
		out.flush()
	
	#---
	
	print_message(f'SUCCESS! See "{fname}" for results\n', False)
	
	sys.stdout = sys.__stdout__
	out.close()

#=======================================================================
#=======================================================================



root = tk.Tk()
root.title('x1fd3')

mode = tk.StringVar()

# mode selector

ttk.Label(
	text = f'{"Select runtype mode":^217}',
	font = ('bold', 16),
	borderwidth = 2,
	relief = 'solid'
).grid(
	row = 0, 
	column = 0
)


ttk.Radiobutton(
	text = 'Point-wise PEC approximation with EMO', 
	value = 'pw_pec_approx', 
	variable = mode, 
	command = lambda: select_mode(mode)
).grid(
	row = 1, 
	column = 0,
	columnspan = 4
)

ttk.Radiobutton(
	text = 'Vib.-rot. levels calculation with point-wise PEC', 
	value = 'lev_calc_pw', 
	variable = mode, 
	command = lambda: select_mode(mode)
).grid(
	row = 2, 
	column = 0,
	columnspan = 4
)


ttk.Radiobutton(
	text = 'Vib.-rot. levels calculation with analytic PEC', 
	value = 'lev_calc_an', 
	variable = mode, 
	command = lambda: select_mode(mode)
).grid(
	row = 3, 
	column = 0,
	columnspan = 4
)

ttk.Radiobutton(
	text = 'Vib.-rot. spectrum calculation with point-wise PEC', 
	value = 'sp_calc_pw', 
	variable = mode, 
	command = lambda: select_mode(mode)
).grid(
	row = 4, 
	column = 0,
	columnspan = 4
)


ttk.Radiobutton(
	text = 'Vib.-rot. spectrum calculation with analytic PEC', 
	value = 'sp_calc_an', 
	variable = mode, 
	command = lambda: select_mode(mode)
).grid(
	row = 5, 
	column = 0,
	columnspan = 4
)

ttk.Radiobutton(
	text = 'Analytic PEC fitting to reproduce given exp. vib.-rot. levels', 
	value = 'fit_pec_to_exp', 
	variable = mode, 
	command = lambda: select_mode(mode)
).grid(
	row = 6, 
	column = 0,
	columnspan = 4
)

frame = ttk.Frame()
frame.columnconfigure(0, minsize = 600)

# input files

hdr_input_files = ttk.Label(
	frame,
	text = f'{"Select input files":^222}',
	font = ('bold', 16),
	borderwidth = 2,
	relief = 'solid'
)

# PW pec

lbl_pw_pec = tk.Label(
	frame,
	text = 'Point-wise PEC, example: pec.txt'
)

file_pw_pec = ttk.Entry(
	frame,
	width = 110,
)

open_pw_pec = ttk.Button(
	frame,
	text = 'Open a file',
	command = lambda: select_file(file_pw_pec)
)

# VR levels calc params

lbl_lev_calc = tk.Label(
	frame,
	text = 'Parameters for vib.-rot. levels calculation, example: vr_level_calc_params.txt'
)

file_lev_calc = ttk.Entry(
	frame,
	width = 110
)

open_lev_calc = ttk.Button(
	frame,
	text = 'Open a file',
	command = lambda: select_file(file_lev_calc)
)

# VR spectrum calc params

lbl_sp_calc = tk.Label(
	frame,
	text = 'Parameters for vib.-rot. spectrum calculation, example: vr_spectrum_calc_params.txt'
)

file_sp_calc = ttk.Entry(
	frame,
	width = 110
)

open_sp_calc = ttk.Button(
	frame,
	text = 'Open a file',
	command = lambda: select_file(file_sp_calc)
)

# VR fit params

lbl_fit_calc = tk.Label(
	frame,
	text = 'Parameters for vib.-rot. levels calculation, example: vr_fit_params.txt'
)

file_fit_calc = ttk.Entry(
	frame,
	width = 110
)

open_fit_calc = ttk.Button(
	frame,
	text = 'Open a file',
	command = lambda: select_file(file_fit_calc)
)

# init EMO pars

lbl_init_pars = tk.Label(
	frame,
	text = 'Initial EMO parameters for PEC approxomation, example: init_params.txt'
)

file_init_pars = ttk.Entry(
	frame,
	width = 110
)

open_init_pars = ttk.Button(
	frame,
	text = 'Open a file',
	command = lambda: select_file(file_init_pars)
)

# fitted EMO pars

lbl_fitted_pars = tk.Label(
	frame,
	text = 'Fitted EMO parameters for levels/spectrum calculation, example: emo_params.txt'
)

file_fitted_pars = ttk.Entry(
	frame,
	width = 110
)

open_fitted_pars = ttk.Button(
	frame,
	text = 'Open a file',
	command = lambda: select_file(file_fitted_pars)
)

# dipole

lbl_pw_dip = tk.Label(
	frame,
	text = 'Point-wise dipole moment, example: dm.txt'
)

file_pw_dip = ttk.Entry(
	frame,
	width = 110
)

open_pw_dip = ttk.Button(
	frame,
	text = 'Open a file',
	command = lambda: select_file(file_pw_dip)
)

# exp data

lbl_exp = tk.Label(
	frame,
	text = 'Experimental vib.-rot. levels, example: levels.txt'
)

file_exp = ttk.Entry(
	frame,
	width = 110
)

open_exp = ttk.Button(
	frame,
	text = 'Open a file',
	command = lambda: select_file(file_exp)
)


# out file

hdr_out = ttk.Label(
	frame,
	text = f'{"Select out file":^223}',
	font = ('bold', 16),
	borderwidth = 2,
	relief = 'solid'
)

lbl_out = tk.Label(
	frame,
	text = 'Output file:'
)

file_out = ttk.Entry(
	frame,
	width = 110
)

open_out = ttk.Button(
	frame,
	text = 'Open a file',
	command = lambda: select_file(file_out)
)

# window for messages

vscroll = tk.Scrollbar(
	frame,
	orient = 'vertical'
)

message_window = tk.Text(
	frame,
	width = 200, 
	height = 20,
	state = 'disabled',
	yscrollcommand = vscroll.set
)

# run

ttk.Style().configure('my.TButton', font = ('bold', 16), foreground = 'red')

run = ttk.Button(
	frame,
	text = 'RUN',
	width = 50,
	style = 'my.TButton',
	command = lambda: run_calc(mode)
)



# main loop

root.mainloop()
