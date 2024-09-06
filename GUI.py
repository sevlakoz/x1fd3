import os
import sys
import tkinter as tk
from tkinter import filedialog
from tkinter import ttk

from funcs import print_input_file, PWcurve, print_pecs,\
                  pec_fit, Parameters, read_expdata,\
                  exp_fit, Levels, MatrixElements

#=======================================================================
#=======================================================================

class MainWindow:
    '''
    class to draw main window
    '''
    def __init__(
        self
    ) -> None:
        '''
        init = blank variables definition
        '''
        self.root = tk.Tk()
        self.mode = tk.StringVar()
        self.frame = ttk.Frame()
        self.hdr_input_files = ttk.Label()
        self.lbl_pw_pec = tk.Label()
        self.file_pw_pec = ttk.Entry()
        self.open_pw_pec = ttk.Button()
        self.lbl_lev_calc = tk.Label()
        self.file_lev_calc = ttk.Entry()
        self.open_lev_calc = ttk.Button()
        self.lbl_sp_calc = tk.Label()
        self.file_sp_calc = ttk.Entry()
        self.open_sp_calc = ttk.Button()
        self.lbl_fit_calc = tk.Label()
        self.file_fit_calc = ttk.Entry()
        self.open_fit_calc = ttk.Button()
        self.lbl_init_params = tk.Label()
        self.file_init_params = ttk.Entry()
        self.open_init_params = ttk.Button()
        self.lbl_fitted_params = tk.Label()
        self.file_fitted_params = ttk.Entry()
        self.open_fitted_params = ttk.Button()
        self.lbl_pw_dip = tk.Label()
        self.file_pw_dip = ttk.Entry()
        self.open_pw_dip = ttk.Button()
        self.lbl_exp = tk.Label()
        self.file_exp = ttk.Entry()
        self.open_exp = ttk.Button()
        self.hdr_out = ttk.Label()
        self.lbl_out = tk.Label()
        self.file_out = ttk.Entry()
        self.open_out = ttk.Button()
        self.vscroll = tk.Scrollbar()
        self.message_window = tk.Text()
        self.run = ttk.Button()

    def select_mode(
        self
    ) -> None:
        '''
        selector mode for main window and redraw frame
        '''
        for widget in self.frame.winfo_children():
            widget.grid_forget()

        self.hdr_input_files.grid(
            row = 100,
            column = 0,
            columnspan = 4
        )

        ttk.Separator(
            self.frame,
            orient = 'horizontal'
        ).grid(
            row = 101,
            column = 0,
            columnspan = 4,
            sticky = 'ew'
        )

        if self.mode.get() in [
            'pw_pec_approx',
            'lev_calc_pw',
            'sp_calc_pw',
            'fit_pec_to_exp'
        ]:
            self.lbl_pw_pec.grid(
                row = 102,
                column = 0,
                sticky = 'e'
            )

            self.file_pw_pec.grid(
                row = 102,
                column = 1
            )

            self.open_pw_pec.grid(
                row = 102,
                column = 2
            )

        if self.mode.get() in [
            'lev_calc_pw',
            'lev_calc_an'
        ]:

            self.lbl_lev_calc.grid(
                row = 103,
                column = 0,
                sticky = 'e'
            )

            self.file_lev_calc.grid(
                row = 103,
                column = 1
            )

            self.open_lev_calc.grid(
                row = 103,
                column = 2
            )

        if self.mode.get() in [
            'sp_calc_pw',
            'sp_calc_an'
        ]:

            self.lbl_sp_calc.grid(
                row = 104,
                column = 0,
                sticky = 'e'
            )

            self.file_sp_calc.grid(
                row = 104,
                column = 1
            )

            self.open_sp_calc.grid(
                row = 104,
                column = 2
            )

        if self.mode.get() in [
            'fit_pec_to_exp'
        ]:

            self.lbl_fit_calc.grid(
                row = 105,
                column = 0,
                sticky = 'e'
            )

            self.file_fit_calc.grid(
                row = 105,
                column = 1
            )

            self.open_fit_calc.grid(
                row = 105,
                column = 2
            )

        if self.mode.get() in [
            'pw_pec_approx'
        ]:
            self.lbl_init_params.grid(
                row = 106,
                column = 0,
                sticky = 'e'
            )

            self.file_init_params.grid(
                row = 106,
                column = 1
            )

            self.open_init_params.grid(
                row = 106,
                column = 2
            )

        if self.mode.get() in [
            'lev_calc_an',
            'sp_calc_an',
            'fit_pec_to_exp'
        ]:
            self.lbl_fitted_params.grid(
                row = 107,
                column = 0,
                sticky = 'e'
            )

            self.file_fitted_params.grid(
                row = 107,
                column = 1
            )

            self.open_fitted_params.grid(
                row = 107,
                column = 2
            )

        if self.mode.get() in [
            'sp_calc_pw',
            'sp_calc_an'
        ]:
            self.lbl_pw_dip.grid(
                row = 108,
                column = 0,
                sticky = 'e'
            )

            self.file_pw_dip.grid(
                row = 108,
                column = 1
            )

            self.open_pw_dip.grid(
                row = 108,
                column = 2
            )

        if self.mode.get() in [
            'fit_pec_to_exp'
        ]:
            self.lbl_exp.grid(
                row = 109,
                column = 0,
                sticky = 'e'
            )

            self.file_exp.grid(
                row = 109,
                column = 1
            )

            self.open_exp.grid(
                row = 109,
                column = 2
            )

        self.hdr_out.grid(
            row = 110,
            column = 0,
            columnspan = 4
        )

        ttk.Separator(
            self.frame,
            orient = 'horizontal'
        ).grid(
            row = 111,
            column = 0,
            columnspan = 4,
            sticky = 'ew'
        )

        self.lbl_out.grid(
            row = 112,
            column = 0,
            sticky = 'e'
        )

        self.file_out.grid(
            row = 112,
            column = 1
        )

        self.open_out.grid(
            row = 112,
            column = 2
        )

        self.vscroll.grid(
            row = 113,
            column = 3,
            sticky = tk.N + tk.S
        )

        self.message_window.grid(
            row = 113,
            column = 0,
            columnspan = 3,
            sticky = tk.W + tk.E
        )

        self.run.grid(
            row = 114,
            column = 0,
            columnspan = 4
        )

        self.frame.grid(
            row = 10,
            column = 0,
            columnspan = 4
        )

    def print_message(
        self,
        string: str,
        prnt: bool = True
    ) -> None:
        '''
        print to window and to stdout
        '''
        if prnt:
            print(string)

        self.message_window.configure(state = 'normal')
        self.message_window.insert('end', string)
        self.message_window.configure(state = 'disabled')

    def select_file(
            self,
            obj: ttk.Entry
        ) -> None:
        '''
        function for tk open file dialog
        '''
        filetypes = (
            ('text files', '*.txt'),
            ('All files', '*.*')
        )

        fname = filedialog.askopenfilename(
            title = 'Open a file',
            filetypes = filetypes
        )

        if fname:
            if os.getcwd() == os.path.dirname(fname):
                fname = os.path.basename(fname)

        obj.delete(0, 'end')
        obj.insert(0, fname)

    def run_calc(
        self
    ) -> None:
        '''
        run selected calculation
        '''
        fname = self.file_out.get()
        if fname:
            if os.path.isfile(fname) and os.path.getsize(fname) > 0:
                self.print_message(f'ERROR: non-empty out file "{fname}" already exists\n', False)
                return
        else:
            self.print_message('ERROR: out file not specified\n', False)
            return

        out = open(fname, 'w', encoding = 'utf-8')
        sys.stdout = out

        #---

        if self.mode.get() == 'pw_pec_approx':

            f_pw_pec = self.file_pw_pec.get()
            f_init_par = self.file_init_params.get()

            # print input
            try:
                print('* Point-wise PEC *')
                print_input_file(f_pw_pec)
                out.flush()
            except BaseException as ex:
                self.print_message(f'ERROR: failed to read input file with point-wise PEC: {str(ex)}\n')
                out.flush()
                return

            try:
                print('* Init EMO parameters *')
                print_input_file(f_init_par)
                out.flush()
            except BaseException as ex:
                self.print_message(f'ERROR: failed to read input file with initial EMO parameters: {str(ex)}\n')
                out.flush()
                return

            # read files
            try:
                pec = PWcurve(f_pw_pec)
            except BaseException as ex:
                self.print_message(f'ERROR: failed to read point-wise PEC: {str(ex)}\n')
                out.flush()
                return

            try:
                params = Parameters()
                params.read_pec_params(f_init_par)
            except BaseException as ex:
                self.print_message(f'ERROR: failed to read initial EMO parameters: {str(ex)}\n')
                out.flush()
                return

            # print initial guess
            print('=== Point-wise PEC approximation ===\n')
            print('Initial guess\n')
            print_pecs(pec, params)
            out.flush()

            # fit
            try:
                params, message, success = pec_fit(pec, params)
                if success:
                    print(f'\nPoint-wise PEC approximation done: {message}')
                    out.flush()
                else:
                    self.print_message(f'ERROR: point-wise PEC approximation FAILED: {message}\n')
                    out.flush()
                    return
            except BaseException as ex:
                self.print_message(f'ERROR: failed to run "pec_fit" function: {str(ex)}\n')
                out.flush()
                return

            # final approximation
            print('\nFitted PEC\n')
            print_pecs(pec, params)
            print('\nFitted parameters\n')
            params.print_pec_params()
            out.flush()

        #---

        if self.mode.get() == 'lev_calc_pw':

            f_vr_par = self.file_lev_calc.get()
            f_pw_pec = self.file_pw_pec.get()

            # print input
            try:
                print('* Parameter for vib.-rot. levels calculation *')
                print_input_file(f_vr_par)
                out.flush()
            except BaseException as ex:
                self.print_message(f'ERROR: failed to read input file with parameter for vib.-rot. levels calculation: {str(ex)}\n')
                out.flush()
                return

            try:
                print('* Point-wise PEC *')
                print_input_file(f_pw_pec)
                out.flush()
            except BaseException as ex:
                self.print_message(f'ERROR: failed to read input file with point-wise PEC: {str(ex)}\n')
                out.flush()
                return

            # read files
            try:
                pec = PWcurve(f_pw_pec)
            except BaseException as ex:
                self.print_message(f'ERROR: failed to read point-wise PEC: {str(ex)}\n')
                out.flush()
                return

            try:
                params = Parameters()
                params.read_vr_calc_params(f_vr_par, 'ENERGY')
            except BaseException as ex:
                self.print_message(f'ERROR: failed to read parameter for vib.-rot. levels calculation: {str(ex)}\n')
                out.flush()
                return

            # calc and print vr levels
            try:
                levels = Levels('pw', params, pec)
            except BaseException as ex:
                self.print_message(f'ERROR: failed to run "vr_solver" function: {str(ex)}\n')
                out.flush()
                return

            levels.print()
            out.flush()

        #---

        if self.mode.get() == 'lev_calc_an':

            f_vr_par = self.file_lev_calc.get()
            f_fit_par = self.file_fitted_params.get()

            # print input
            try:
                print('* Parameter for vib.-rot. levels calculation *')
                print_input_file(f_vr_par)
                out.flush()
            except BaseException as ex:
                self.print_message(f'ERROR: failed to read input file with parameter for vib.-rot. levels calculation: {str(ex)}\n')
                out.flush()
                return

            try:
                print('* Fitted EMO parameters *')
                print_input_file(f_fit_par)
                out.flush()
            except BaseException as ex:
                self.print_message(f'ERROR: failed to read input file with fitted EMO parameters: {str(ex)}\n')
                out.flush()
                return

            # read files
            try:
                params = Parameters()
                params.read_vr_calc_params(f_vr_par, 'ENERGY')
            except BaseException as ex:
                self.print_message(f'ERROR: failed to read parameter for vib.-rot. levels calculation: {str(ex)}\n')
                out.flush()
                return

            try:
                params.read_pec_params(f_fit_par)
            except BaseException as ex:
                self.print_message(f'ERROR: failed to read fitted EMO parameters: {str(ex)}\n')
                out.flush()
                return


            # calc and print vr levels
            try:
                levels = Levels('an', params)
            except BaseException as ex:
                self.print_message(f'ERROR: failed to run "vr_solver" function: {str(ex)}\n')
                out.flush()
                return

            levels.print()
            out.flush()

        #---

        if self.mode.get() == 'sp_calc_pw':

            f_vr_par = self.file_sp_calc.get()
            f_pw_pec = self.file_pw_pec.get()
            f_pw_dm = self.file_pw_dip.get()

            # print input
            try:
                print('* Parameters for vib.-rot. spectrum calculation *')
                print_input_file(f_vr_par)
                out.flush()
            except BaseException as ex:
                self.print_message(f'ERROR: failed to read input file with parameter for vib.-rot. spectrum calculation: {str(ex)}\n')
                out.flush()
                return

            try:
                print('* Point-wise PEC *')
                print_input_file(f_pw_pec)
                out.flush()
            except BaseException as ex:
                self.print_message(f'ERROR: failed to read input file with point-wise PEC: {str(ex)}\n')
                out.flush()
                return

            try:
                print('* Point-wise dipole moment *')
                print_input_file(f_pw_dm)
                out.flush()
            except BaseException as ex:
                self.print_message(f'ERROR: failed to read input file with point-wise dipole moment: {str(ex)}\n')
                out.flush()
                return

            # read files
            try:
                pec = PWcurve(f_pw_pec)
            except BaseException as ex:
                self.print_message(f'ERROR: failed to read point-wise PEC: {str(ex)}\n')
                out.flush()
                return

            try:
                dm = PWcurve(f_pw_dm)
            except BaseException as ex:
                self.print_message(f'ERROR: failed to read point-wise dipole moment: {str(ex)}\n')
                out.flush()
                return

            try:
                params = Parameters()
                params.read_vr_calc_params(f_vr_par, 'SPECTRUM')
            except BaseException as ex:
                self.print_message(f'ERROR: failed to read parameter for vib.-rot. spectrum calculation: {str(ex)}\n')
                out.flush()
                return

            # calc vr levels
            try:
                levels = Levels('pw', params, pec)
            except BaseException as ex:
                self.print_message(f'ERROR: failed to run "vr_solver" function: {str(ex)}\n')
                out.flush()
                return

            # calc and print integrals
            try:
                matrix_elements = MatrixElements(params, levels, dm)
            except BaseException as ex:
                self.print_message(f'ERROR: failed to run "matrix_elements" function: {str(ex)}\n')
                out.flush()
                return

            matrix_elements.print()
            out.flush()

        #---

        if self.mode.get() == 'sp_calc_an':

            f_vr_par = self.file_sp_calc.get()
            f_fit_par = self.file_fitted_params.get()
            f_pw_dm = self.file_pw_dip.get()

            # print input
            try:
                print('* Parameters for vib.-rot. spectrum calculation *')
                print_input_file(f_vr_par)
                out.flush()
            except BaseException as ex:
                self.print_message(f'ERROR: failed to read input file with parameter for vib.-rot. spectrum calculation: {str(ex)}\n')
                out.flush()
                return

            try:
                print('* Fitted EMO parameters *')
                print_input_file(f_fit_par)
                out.flush()
            except BaseException as ex:
                self.print_message(f'ERROR: failed to read input file with fitted EMO parameters: {str(ex)}\n')
                out.flush()
                return

            try:
                print('* Point-wise dipole moment *')
                print_input_file(f_pw_dm)
                out.flush()
            except BaseException as ex:
                self.print_message(f'ERROR: failed to read input file with point-wise dipole moment: {str(ex)}\n')
                out.flush()
                return

            # read files
            try:
                params = Parameters()
                params.read_vr_calc_params(f_vr_par, 'SPECTRUM')
            except BaseException as ex:
                self.print_message(f'ERROR: failed to read parameter for vib.-rot. spectrum calculation: {str(ex)}\n')
                out.flush()
                return

            try:
                params.read_pec_params(f_fit_par)
            except BaseException as ex:
                self.print_message(f'ERROR: failed to read fitted EMO parameters: {str(ex)}\n')
                out.flush()
                return

            try:
                dm = PWcurve(f_pw_dm)
            except BaseException as ex:
                self.print_message(f'ERROR: failed to read point-wise dipole moment: {str(ex)}\n')
                out.flush()
                return

            # calc vr levels
            try:
                levels = Levels('an', params)
            except BaseException as ex:
                self.print_message(f'ERROR: failed to run "vr_solver" function: {str(ex)}\n')
                out.flush()
                return

            # calc and print integrals
            try:
                matrix_elements = MatrixElements(params, levels, dm)
            except BaseException as ex:
                self.print_message(f'ERROR: failed to run "matrix_elements" function: {str(ex)}\n')
                out.flush()
                return

            matrix_elements.print()
            out.flush()

        #---

        if self.mode.get() == 'fit_pec_to_exp':

            f_vr_par = self.file_fit_calc.get()
            f_fit_par = self.file_fitted_params.get()
            f_pw_pec = self.file_pw_pec.get()
            f_epx_lev = self.file_exp.get()

            # print input
            try:
                print('* Parameters for PEC fit to exp. levels *')
                print_input_file(f_vr_par)
                out.flush()
            except BaseException as ex:
                self.print_message(f'ERROR: failed to read input file with parameter for PEC fit to exp. levels: {str(ex)}\n')
                out.flush()
                return

            try:
                print('* Fitted EMO parameters *')
                print_input_file(f_fit_par)
                out.flush()
            except BaseException as ex:
                self.print_message(f'ERROR: failed to read input file with fitted EMO parameters: {str(ex)}\n')
                out.flush()
                return

            try:
                print('* Point-wise PEC *')
                print_input_file(f_pw_pec)
                out.flush()
            except BaseException as ex:
                self.print_message(f'ERROR: failed to read input file with point-wise PEC: {str(ex)}\n')
                out.flush()
                return

            try:
                print('* Exp. levels *')
                print_input_file(f_epx_lev)
                out.flush()
            except BaseException as ex:
                self.print_message(f'ERROR: failed to read input file with exp. vib.-rot. levels: {str(ex)}\n')
                out.flush()
                return

            # read files
            try:
                pec = PWcurve(f_pw_pec)
            except BaseException as ex:
                self.print_message(f'ERROR: failed to read point-wise PEC: {str(ex)}\n')
                out.flush()
                return

            try:
                params = Parameters()
                params.read_vr_calc_params(f_vr_par, 'FIT')
            except BaseException as ex:
                self.print_message(f'ERROR: failed to read parameter for PEC fit to exp. levels: {str(ex)}\n')
                out.flush()
                return

            try:
                params.read_pec_params(f_fit_par)
            except BaseException as ex:
                self.print_message(f'ERROR: failed to read fitted EMO parameters: {str(ex)}\n')
                out.flush()
                return

            try:
                expdata = read_expdata(f_epx_lev)
            except BaseException as ex:
                self.print_message(f'ERROR: failed to read exp. vib.-rot. levels: {str(ex)}\n')
                out.flush()
                return

            params['jmax'] = max(expdata.keys())

            print('=== Fit PEC to reproduce exp. data ===\n')

            # print initial guess
            print('Initial guess')
            try:
                levels = Levels('an', params)
            except BaseException as ex:
                self.print_message(f'ERROR: failed to run "vr_solver" function: {str(ex)}\n')
                out.flush()
                return

            levels.print_with_expdata(expdata)
            print_pecs(pec, params)
            out.flush()

            # fit
            try:
                params, message, success = exp_fit(params, pec, expdata)
                if success:
                    print(f'\nPEC fit to exp. levels done: {message}')
                    out.flush()
                else:
                    self.print_message(f'ERROR: PEC fit to exp. levels FAILED: {message}')
                    out.flush()
                    return
            except BaseException as ex:
                self.print_message(f'ERROR: failed to run "exp_fit" function: {str(ex)}\n')
                out.flush()
                return

            # print final results
            print('\nFit results')
            try:
                levels = Levels('an', params)
            except BaseException as ex:
                self.print_message(f'ERROR: failed to run "vr_solver" function: {str(ex)}\n')
                out.flush()
                return
            levels.print_with_expdata(expdata)
            print_pecs(pec, params)
            print('\nFitted parameters\n')
            params.print_pec_params()
            out.flush()

        #---

        self.print_message(f'SUCCESS! See "{fname}" for results\n', False)

        sys.stdout = sys.__stdout__
        out.close()
#=======================================================================
#=======================================================================


def main() -> None:
    '''
    draw radiobutton for mode selection, call select_mode to draw other elements inside frame
    '''
    main_window = MainWindow()

    main_window.root.title('x1fd3')
    main_window.root.resizable(False, False)

    # mode selector
    ttk.Label(
        text = 'Select runtype mode',
        font = ('bold', 16)
    ).grid(
        row = 0,
        column = 0,
        columnspan = 4
    )

    ttk.Separator(
        orient = 'horizontal'
    ).grid(
        row = 1,
        column = 0,
        columnspan = 4,
        sticky = 'ew'
    )

    ttk.Radiobutton(
        text = 'Point-wise PEC approximation with EMO',
        value = 'pw_pec_approx',
        variable = main_window.mode,
        command = main_window.select_mode
    ).grid(
        row = 2,
        column = 2,
        sticky = 'w'
    )

    ttk.Radiobutton(
        text = 'Vib.-rot. levels calculation with point-wise PEC',
        value = 'lev_calc_pw',
        variable = main_window.mode,
        command = main_window.select_mode
    ).grid(
        row = 3,
        column = 2,
        sticky = 'w'
    )


    ttk.Radiobutton(
        text = 'Vib.-rot. levels calculation with analytic PEC (EMO)',
        value = 'lev_calc_an',
        variable = main_window.mode,
        command = main_window.select_mode
    ).grid(
        row = 4,
        column = 2,
        sticky = 'w'
    )

    ttk.Radiobutton(
        text = 'Vib.-rot. spectrum calculation with point-wise PEC',
        value = 'sp_calc_pw',
        variable = main_window.mode,
        command = main_window.select_mode
    ).grid(
        row = 5,
        column = 2,
        sticky = 'w'
    )


    ttk.Radiobutton(
        text = 'Vib.-rot. spectrum calculation with analytic PEC (EMO)',
        value = 'sp_calc_an',
        variable = main_window.mode,
        command = main_window.select_mode
    ).grid(
        row = 6,
        column = 2,
        sticky = 'w'
    )

    ttk.Radiobutton(
        text = 'Analytic PEC (EMO) fitting to reproduce experimental vib.-rot. levels',
        value = 'fit_pec_to_exp',
        variable = main_window.mode,
        command = main_window.select_mode
    ).grid(
        row = 7,
        column = 2,
        sticky = 'w'
    )
   
    main_window.frame.columnconfigure(0, minsize = 600)

    #
    # frame
    #

    # input files

    main_window.hdr_input_files = ttk.Label(
        main_window.frame,
        text = 'Select input files',
        font = ('bold', 16)
    )

    # PW pec

    main_window.lbl_pw_pec = tk.Label(
        main_window.frame,
        text = 'Point-wise PEC, example: pw_pec.txt'
    )

    main_window.file_pw_pec = ttk.Entry(
        main_window.frame,
        width = 110,
    )

    main_window.open_pw_pec = ttk.Button(
        main_window.frame,
        text = 'Open a file',
        command = lambda: main_window.select_file(main_window.file_pw_pec)
    )

    # VR levels calc params

    main_window.lbl_lev_calc = tk.Label(
        main_window.frame,
        text = 'Parameters for vib.-rot. levels calculation, example: vr_level_calc_params.txt'
    )

    main_window.file_lev_calc = ttk.Entry(
        main_window.frame,
        width = 110
    )

    main_window.open_lev_calc = ttk.Button(
        main_window.frame,
        text = 'Open a file',
        command = lambda: main_window.select_file(main_window.file_lev_calc)
    )

    # VR spectrum calc params

    main_window.lbl_sp_calc = tk.Label(
        main_window.frame,
        text = 'Parameters for vib.-rot. spectrum calculation, example: vr_spectrum_calc_params.txt'
    )

    main_window.file_sp_calc = ttk.Entry(
        main_window.frame,
        width = 110
    )

    main_window.open_sp_calc = ttk.Button(
        main_window.frame,
        text = 'Open a file',
        command = lambda: main_window.select_file(main_window.file_sp_calc)
    )

    # VR fit params

    main_window.lbl_fit_calc = tk.Label(
        main_window.frame,
        text = 'Parameters for vib.-rot. levels calculation, example: vr_fit_params.txt'
    )

    main_window.file_fit_calc = ttk.Entry(
        main_window.frame,
        width = 110
    )

    main_window.open_fit_calc = ttk.Button(
        main_window.frame,
        text = 'Open a file',
        command = lambda: main_window.select_file(main_window.file_fit_calc)
    )

    # init EMO params

    main_window.lbl_init_params = tk.Label(
        main_window.frame,
        text = 'Initial EMO parameters for PEC approxomation, example: init_emo_params.txt'
    )

    main_window.file_init_params = ttk.Entry(
        main_window.frame,
        width = 110
    )

    main_window.open_init_params = ttk.Button(
        main_window.frame,
        text = 'Open a file',
        command = lambda: main_window.select_file(main_window.file_init_params)
    )

    # fitted EMO params

    main_window.lbl_fitted_params = tk.Label(
        main_window.frame,
        text = 'Fitted EMO parameters for levels/spectrum calculation, example: fitted_emo_params.txt'
    )

    main_window.file_fitted_params = ttk.Entry(
        main_window.frame,
        width = 110
    )

    main_window.open_fitted_params = ttk.Button(
        main_window.frame,
        text = 'Open a file',
        command = lambda: main_window.select_file(main_window.file_fitted_params)
    )

    # dipole

    main_window.lbl_pw_dip = tk.Label(
        main_window.frame,
        text = 'Point-wise dipole moment, example: pw_dm.txt'
    )

    main_window.file_pw_dip = ttk.Entry(
        main_window.frame,
        width = 110
    )

    main_window.open_pw_dip = ttk.Button(
        main_window.frame,
        text = 'Open a file',
        command = lambda: main_window.select_file(main_window.file_pw_dip)
    )

    # exp data

    main_window.lbl_exp = tk.Label(
        main_window.frame,
        text = 'Experimental vib.-rot. levels, example: levels.txt'
    )

    main_window.file_exp = ttk.Entry(
        main_window.frame,
        width = 110
    )

    main_window.open_exp = ttk.Button(
        main_window.frame,
        text = 'Open a file',
        command = lambda: main_window.select_file(main_window.file_exp)
    )


    # out file

    main_window.hdr_out = ttk.Label(
        main_window.frame,
        text = 'Select out file',
        font = ('bold', 16)
    )

    main_window.lbl_out = tk.Label(
        main_window.frame,
        text = 'Output file:'
    )

    main_window.file_out = ttk.Entry(
        main_window.frame,
        width = 110
    )

    main_window.open_out = ttk.Button(
        main_window.frame,
        text = 'Open a file',
        command = lambda: main_window.select_file(main_window.file_out)
    )

    # window for messages

    main_window.vscroll = tk.Scrollbar(
        main_window.frame,
        orient = 'vertical'
    )

    main_window.message_window = tk.Text(
        main_window.frame,
        width = 160,
        height = 20,
        state = 'disabled',
        yscrollcommand = main_window.vscroll.set
    )

    # run

    ttk.Style().configure('my.TButton', font = ('bold', 16), foreground = 'red')

    main_window.run = ttk.Button(
        main_window.frame,
        text = 'RUN',
        width = 50,
        style = 'my.TButton',
        command = main_window.run_calc
    )

    # main loop for tk
    main_window.root.mainloop()

if __name__ == "__main__":
    main()
