#import sys
from os import getcwd
from os.path import isfile, getsize, dirname, basename
import tkinter as tk
from tkinter import filedialog
from tkinter import ttk

from x1fd3.base.p_w_curve import PWCurve
from x1fd3.base.parameters import Parameters
from x1fd3.base.levels import Levels
from x1fd3.base.matrix_elements import MatrixElements
from x1fd3.base.logger import Logger
from x1fd3.base.print_funcs import print_input_file, print_pecs
from x1fd3.base.fit_funcs import pec_fit, exp_fit
from x1fd3.base.read_expdata import read_expdata

class MainWindow:
    '''
    class to draw main window
    '''
    def __init__(
        self
    ) -> None:
        '''
        draw radiobutton for mode selection, call select_mode to draw other elements inside frame
        '''
        self.root = tk.Tk()
        self.mode = tk.StringVar()
        self.frame = ttk.Frame()

        self.root.title('x1fd3')
        self.root.resizable(False, False)

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
            value = 'PecApprox',
            variable = self.mode,
            command = self.select_mode
        ).grid(
            row = 2,
            column = 2,
            sticky = 'w'
        )

        ttk.Radiobutton(
            text = 'Vib.-rot. levels calculation with point-wise PEC',
            value = 'LevelsPW',
            variable = self.mode,
            command = self.select_mode
        ).grid(
            row = 3,
            column = 2,
            sticky = 'w'
        )


        ttk.Radiobutton(
            text = 'Vib.-rot. levels calculation with analytic PEC (EMO)',
            value = 'LevelsAn',
            variable = self.mode,
            command = self.select_mode
        ).grid(
            row = 4,
            column = 2,
            sticky = 'w'
        )

        ttk.Radiobutton(
            text = 'Vib.-rot. spectrum calculation with point-wise PEC',
            value = 'SpectrumPW',
            variable = self.mode,
            command = self.select_mode
        ).grid(
            row = 5,
            column = 2,
            sticky = 'w'
        )


        ttk.Radiobutton(
            text = 'Vib.-rot. spectrum calculation with analytic PEC (EMO)',
            value = 'SpectrumAn',
            variable = self.mode,
            command = self.select_mode
        ).grid(
            row = 6,
            column = 2,
            sticky = 'w'
        )

        ttk.Radiobutton(
            text = 'Analytic PEC (EMO) fitting to reproduce experimental vib.-rot. levels',
            value = 'FitExp',
            variable = self.mode,
            command = self.select_mode
        ).grid(
            row = 7,
            column = 2,
            sticky = 'w'
        )

        self.frame.columnconfigure(0, minsize = 600)

        #
        # frame
        #

        # input files

        self.hdr_input_files = ttk.Label(
            self.frame,
            text = 'Select input files',
            font = ('bold', 16)
        )

        # PW pec

        self.lbl_pw_pec = tk.Label(
            self.frame,
            text = 'Point-wise PEC, example: pw_pec.txt'
        )

        self.file_pw_pec = ttk.Entry(
            self.frame,
            width = 110,
        )

        self.open_pw_pec = ttk.Button(
            self.frame,
            text = 'Open a file',
            command = lambda: self.select_file(self.file_pw_pec)
        )

        # VR levels calc params

        self.lbl_lev_calc = tk.Label(
            self.frame,
            text = 'Parameters for vib.-rot. levels calculation, example: vr_level_calc_params.txt'
        )

        self.file_lev_calc = ttk.Entry(
            self.frame,
            width = 110
        )

        self.open_lev_calc = ttk.Button(
            self.frame,
            text = 'Open a file',
            command = lambda: self.select_file(self.file_lev_calc)
        )

        # VR spectrum calc params

        self.lbl_sp_calc = tk.Label(
            self.frame,
            text = 'Parameters for vib.-rot. spectrum calculation, example: vr_spectrum_calc_params.txt'
        )

        self.file_sp_calc = ttk.Entry(
            self.frame,
            width = 110
        )

        self.open_sp_calc = ttk.Button(
            self.frame,
            text = 'Open a file',
            command = lambda: self.select_file(self.file_sp_calc)
        )

        # VR fit params

        self.lbl_fit_calc = tk.Label(
            self.frame,
            text = 'Parameters for vib.-rot. levels calculation, example: vr_fit_params.txt'
        )

        self.file_fit_calc = ttk.Entry(
            self.frame,
            width = 110
        )

        self.open_fit_calc = ttk.Button(
            self.frame,
            text = 'Open a file',
            command = lambda: self.select_file(self.file_fit_calc)
        )

        # init EMO params

        self.lbl_init_params = tk.Label(
            self.frame,
            text = 'Initial EMO parameters for PEC approxomation, example: init_emo_params.txt'
        )

        self.file_init_params = ttk.Entry(
            self.frame,
            width = 110
        )

        self.open_init_params = ttk.Button(
            self.frame,
            text = 'Open a file',
            command = lambda: self.select_file(self.file_init_params)
        )

        # fitted EMO params

        self.lbl_fitted_params = tk.Label(
            self.frame,
            text = 'Fitted EMO parameters for levels/spectrum calculation, example: fitted_emo_params.txt'
        )

        self.file_fitted_params = ttk.Entry(
            self.frame,
            width = 110
        )

        self.open_fitted_params = ttk.Button(
            self.frame,
            text = 'Open a file',
            command = lambda: self.select_file(self.file_fitted_params)
        )

        # dipole

        self.lbl_pw_dip = tk.Label(
            self.frame,
            text = 'Point-wise dipole moment, example: pw_dm.txt'
        )

        self.file_pw_dip = ttk.Entry(
            self.frame,
            width = 110
        )

        self.open_pw_dip = ttk.Button(
            self.frame,
            text = 'Open a file',
            command = lambda: self.select_file(self.file_pw_dip)
        )

        # exp data

        self.lbl_exp = tk.Label(
            self.frame,
            text = 'Experimental vib.-rot. levels, example: exp_levels.txt'
        )

        self.file_exp = ttk.Entry(
            self.frame,
            width = 110
        )

        self.open_exp = ttk.Button(
            self.frame,
            text = 'Open a file',
            command = lambda: self.select_file(self.file_exp)
        )


        # out file

        self.hdr_out = ttk.Label(
            self.frame,
            text = 'Select out file',
            font = ('bold', 16)
        )

        self.lbl_out = tk.Label(
            self.frame,
            text = 'Output file:'
        )

        self.file_out = ttk.Entry(
            self.frame,
            width = 110
        )

        self.open_out = ttk.Button(
            self.frame,
            text = 'Open a file',
            command = lambda: self.select_file(self.file_out)
        )

        # window for messages

        self.vscroll = tk.Scrollbar(
            self.frame,
            orient = 'vertical'
        )

        self.message_window = tk.Text(
            self.frame,
            width = 160,
            height = 20,
            state = 'disabled',
            yscrollcommand = self.vscroll.set
        )

        # run

        ttk.Style().configure('my.TButton', font = ('bold', 16), foreground = 'red')

        self.run = ttk.Button(
            self.frame,
            text = 'RUN',
            width = 50,
            style = 'my.TButton',
            command = self.run_calc
        )

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
            'PecApprox',
            'LevelsPW',
            'SpectrumPW',
            'FitExp'
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
            'LevelsPW',
            'LevelsAn'
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
            'SpectrumPW',
            'SpectrumAn'
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
            'FitExp'
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
            'PecApprox'
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
            'LevelsAn',
            'SpectrumAn',
            'FitExp'
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
            'SpectrumPW',
            'SpectrumAn'
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
            'FitExp'
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
        out: Logger = Logger()
    ) -> None:
        '''
        print to window and to out
        '''
        self.message_window.configure(state = 'normal')
        self.message_window.insert('end', string)
        self.message_window.configure(state = 'disabled')

        if out.fname:
            out.print(string)

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
            if getcwd() == dirname(fname):
                fname = basename(fname)

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
            if isfile(fname) and getsize(fname) > 0:
                self.print_message(f'ERROR: non-empty out file "{fname}" already exists\n')
                return
        else:
            self.print_message('ERROR: out file not specified\n')
            return

        # redirect stdout to file, because of print in funcs in base module
        out = Logger(fname, True)
        #open(fname, 'w', encoding = 'utf-8')
        #sys.stdout = out

        #---

        if self.mode.get() == 'PecApprox':

            f_pw_pec = self.file_pw_pec.get()
            f_init_par = self.file_init_params.get()

            # print input
            try:
                out.print('* Point-wise PEC *')
                print_input_file(out, f_pw_pec)
            except BaseException as ex: # pylint: disable = W0718
                self.print_message(f'ERROR: failed to read input file with point-wise PEC: {str(ex)}\n', out)
                return

            try:
                out.print('* Init EMO parameters *')
                print_input_file(out, f_init_par)
            except BaseException as ex: # pylint: disable = W0718
                self.print_message(f'ERROR: failed to read input file with initial EMO parameters: {str(ex)}\n', out)
                return

            # read files
            try:
                pec = PWCurve(f_pw_pec)
            except BaseException as ex: # pylint: disable = W0718
                self.print_message(f'ERROR: failed to read point-wise PEC: {str(ex)}\n', out)
                return

            try:
                params = Parameters()
                params.read_pec_params(f_init_par)
            except BaseException as ex: # pylint: disable = W0718
                self.print_message(f'ERROR: failed to read initial EMO parameters: {str(ex)}\n', out)
                return

            # print initial guess
            out.print('=== Point-wise PEC approximation ===\n')
            out.print('Initial guess\n')
            print_pecs(out, pec, params)

            # fit
            try:
                params, message, success = pec_fit(pec, params)
                if success:
                    out.print(f'\nPoint-wise PEC approximation done: {message}')
                else:
                    self.print_message(f'ERROR: point-wise PEC approximation FAILED: {message}\n', out)
                    return
            except BaseException as ex: # pylint: disable = W0718
                self.print_message(f'ERROR: failed to run "pec_fit" function: {str(ex)}\n', out)
                return

            # final approximation
            out.print('\nFitted PEC\n')
            print_pecs(out, pec, params)
            out.print('\nFitted parameters\n')
            params.print_pec_params(out)

        #---

        if self.mode.get() == 'LevelsPW':

            f_vr_par = self.file_lev_calc.get()
            f_pw_pec = self.file_pw_pec.get()

            # print input
            try:
                out.print('* Parameter for vib.-rot. levels calculation *')
                print_input_file(out, f_vr_par)
            except BaseException as ex: # pylint: disable = W0718
                self.print_message(f'ERROR: failed to read input file with parameter for vib.-rot. levels calculation: {str(ex)}\n', out)
                return

            try:
                out.print('* Point-wise PEC *')
                print_input_file(out, f_pw_pec)
            except BaseException as ex: # pylint: disable = W0718
                self.print_message(f'ERROR: failed to read input file with point-wise PEC: {str(ex)}\n', out)
                return

            # read files
            try:
                pec = PWCurve(f_pw_pec)
            except BaseException as ex: # pylint: disable = W0718
                self.print_message(f'ERROR: failed to read point-wise PEC: {str(ex)}\n', out)
                return

            try:
                params = Parameters()
                params.read_vr_calc_params(f_vr_par, 'ENERGY')
            except BaseException as ex: # pylint: disable = W0718
                self.print_message(f'ERROR: failed to read parameter for vib.-rot. levels calculation: {str(ex)}\n', out)
                return

            # calc and print vr levels
            try:
                levels = Levels('pw', params, pec)
            except BaseException as ex: # pylint: disable = W0718
                self.print_message(f'ERROR: failed to run "vr_solver" function: {str(ex)}\n', out)
                return

            levels.print(out)

        #---

        if self.mode.get() == 'LevelsAn':

            f_vr_par = self.file_lev_calc.get()
            f_fit_par = self.file_fitted_params.get()

            # print input
            try:
                out.print('* Parameter for vib.-rot. levels calculation *')
                print_input_file(out, f_vr_par)
            except BaseException as ex: # pylint: disable = W0718
                self.print_message(f'ERROR: failed to read input file with parameter for vib.-rot. levels calculation: {str(ex)}\n', out)
                return

            try:
                out.print('* Fitted EMO parameters *')
                print_input_file(out, f_fit_par)
            except BaseException as ex: # pylint: disable = W0718
                self.print_message(f'ERROR: failed to read input file with fitted EMO parameters: {str(ex)}\n', out)
                return

            # read files
            try:
                params = Parameters()
                params.read_vr_calc_params(f_vr_par, 'ENERGY')
            except BaseException as ex: # pylint: disable = W0718
                self.print_message(f'ERROR: failed to read parameter for vib.-rot. levels calculation: {str(ex)}\n', out)
                return

            try:
                params.read_pec_params(f_fit_par)
            except BaseException as ex: # pylint: disable = W0718
                self.print_message(f'ERROR: failed to read fitted EMO parameters: {str(ex)}\n', out)
                return


            # calc and print vr levels
            try:
                levels = Levels('an', params)
            except BaseException as ex: # pylint: disable = W0718
                self.print_message(f'ERROR: failed to run "vr_solver" function: {str(ex)}\n', out)
                return

            levels.print(out)

        #---

        if self.mode.get() == 'SpectrumPW':

            f_vr_par = self.file_sp_calc.get()
            f_pw_pec = self.file_pw_pec.get()
            f_pw_dm = self.file_pw_dip.get()

            # print input
            try:
                out.print('* Parameters for vib.-rot. spectrum calculation *')
                print_input_file(out, f_vr_par)
            except BaseException as ex: # pylint: disable = W0718
                self.print_message(f'ERROR: failed to read input file with parameter for vib.-rot. spectrum calculation: {str(ex)}\n', out)
                return

            try:
                out.print('* Point-wise PEC *')
                print_input_file(out, f_pw_pec)
            except BaseException as ex: # pylint: disable = W0718
                self.print_message(f'ERROR: failed to read input file with point-wise PEC: {str(ex)}\n', out)
                return

            try:
                out.print('* Point-wise dipole moment *')
                print_input_file(out, f_pw_dm)
            except BaseException as ex: # pylint: disable = W0718
                self.print_message(f'ERROR: failed to read input file with point-wise dipole moment: {str(ex)}\n', out)
                return

            # read files
            try:
                pec = PWCurve(f_pw_pec)
            except BaseException as ex: # pylint: disable = W0718
                self.print_message(f'ERROR: failed to read point-wise PEC: {str(ex)}\n', out)
                return

            try:
                dm = PWCurve(f_pw_dm)
            except BaseException as ex: # pylint: disable = W0718
                self.print_message(f'ERROR: failed to read point-wise dipole moment: {str(ex)}\n', out)
                return

            try:
                params = Parameters()
                params.read_vr_calc_params(f_vr_par, 'SPECTRUM')
            except BaseException as ex: # pylint: disable = W0718
                self.print_message(f'ERROR: failed to read parameter for vib.-rot. spectrum calculation: {str(ex)}\n', out)
                return

            # calc vr levels
            try:
                levels = Levels('pw', params, pec)
            except BaseException as ex: # pylint: disable = W0718
                self.print_message(f'ERROR: failed to run "vr_solver" function: {str(ex)}\n', out)
                return

            # calc and print integrals
            try:
                matrix_elements = MatrixElements(params, levels, dm)
            except BaseException as ex: # pylint: disable = W0718
                self.print_message(f'ERROR: failed to run "matrix_elements" function: {str(ex)}\n', out)
                return

            matrix_elements.print(out)

        #---

        if self.mode.get() == 'SpectrumAn':

            f_vr_par = self.file_sp_calc.get()
            f_fit_par = self.file_fitted_params.get()
            f_pw_dm = self.file_pw_dip.get()

            # print input
            try:
                out.print('* Parameters for vib.-rot. spectrum calculation *')
                print_input_file(out, f_vr_par)
            except BaseException as ex: # pylint: disable = W0718
                self.print_message(f'ERROR: failed to read input file with parameter for vib.-rot. spectrum calculation: {str(ex)}\n', out)
                return

            try:
                out.print('* Fitted EMO parameters *')
                print_input_file(out, f_fit_par)
            except BaseException as ex: # pylint: disable = W0718
                self.print_message(f'ERROR: failed to read input file with fitted EMO parameters: {str(ex)}\n', out)
                return

            try:
                out.print('* Point-wise dipole moment *')
                print_input_file(out, f_pw_dm)
            except BaseException as ex: # pylint: disable = W0718
                self.print_message(f'ERROR: failed to read input file with point-wise dipole moment: {str(ex)}\n', out)
                return

            # read files
            try:
                params = Parameters()
                params.read_vr_calc_params(f_vr_par, 'SPECTRUM')
            except BaseException as ex: # pylint: disable = W0718
                self.print_message(f'ERROR: failed to read parameter for vib.-rot. spectrum calculation: {str(ex)}\n', out)
                return

            try:
                params.read_pec_params(f_fit_par)
            except BaseException as ex: # pylint: disable = W0718
                self.print_message(f'ERROR: failed to read fitted EMO parameters: {str(ex)}\n', out)
                return

            try:
                dm = PWCurve(f_pw_dm)
            except BaseException as ex: # pylint: disable = W0718
                self.print_message(f'ERROR: failed to read point-wise dipole moment: {str(ex)}\n', out)
                return

            # calc vr levels
            try:
                levels = Levels('an', params)
            except BaseException as ex: # pylint: disable = W0718
                self.print_message(f'ERROR: failed to run "vr_solver" function: {str(ex)}\n', out)
                return

            # calc and print integrals
            try:
                matrix_elements = MatrixElements(params, levels, dm)
            except BaseException as ex: # pylint: disable = W0718
                self.print_message(f'ERROR: failed to run "matrix_elements" function: {str(ex)}\n', out)
                return

            matrix_elements.print(out)

        #---

        if self.mode.get() == 'FitExp':

            f_vr_par = self.file_fit_calc.get()
            f_fit_par = self.file_fitted_params.get()
            f_pw_pec = self.file_pw_pec.get()
            f_epx_lev = self.file_exp.get()

            # print input
            try:
                out.print('* Parameters for PEC fit to exp. levels *')
                print_input_file(out, f_vr_par)
            except BaseException as ex: # pylint: disable = W0718
                self.print_message(f'ERROR: failed to read input file with parameter for PEC fit to exp. levels: {str(ex)}\n', out)
                return

            try:
                out.print('* Fitted EMO parameters *')
                print_input_file(out, f_fit_par)
            except BaseException as ex: # pylint: disable = W0718
                self.print_message(f'ERROR: failed to read input file with fitted EMO parameters: {str(ex)}\n', out)
                return

            try:
                out.print('* Point-wise PEC *')
                print_input_file(out, f_pw_pec)
            except BaseException as ex: # pylint: disable = W0718
                self.print_message(f'ERROR: failed to read input file with point-wise PEC: {str(ex)}\n', out)
                return

            try:
                out.print('* Exp. levels *')
                print_input_file(out, f_epx_lev)
            except BaseException as ex: # pylint: disable = W0718
                self.print_message(f'ERROR: failed to read input file with exp. vib.-rot. levels: {str(ex)}\n', out)
                return

            # read files
            try:
                pec = PWCurve(f_pw_pec)
            except BaseException as ex: # pylint: disable = W0718
                self.print_message(f'ERROR: failed to read point-wise PEC: {str(ex)}\n', out)
                return

            try:
                params = Parameters()
                params.read_vr_calc_params(f_vr_par, 'FIT')
            except BaseException as ex: # pylint: disable = W0718
                self.print_message(f'ERROR: failed to read parameter for PEC fit to exp. levels: {str(ex)}\n', out)
                return

            try:
                params.read_pec_params(f_fit_par)
            except BaseException as ex: # pylint: disable = W0718
                self.print_message(f'ERROR: failed to read fitted EMO parameters: {str(ex)}\n', out)
                return

            try:
                expdata = read_expdata(f_epx_lev)
            except BaseException as ex: # pylint: disable = W0718
                self.print_message(f'ERROR: failed to read exp. vib.-rot. levels: {str(ex)}\n', out)
                return

            params['jmax'] = max(expdata.keys())

            out.print('=== Fit PEC to reproduce exp. data ===\n')

            # print initial guess
            out.print('Initial guess')
            try:
                levels = Levels('an', params)
            except BaseException as ex: # pylint: disable = W0718
                self.print_message(f'ERROR: failed to run "vr_solver" function: {str(ex)}\n', out)
                return

            levels.print_with_expdata(out, expdata)
            print_pecs(out, pec, params)

            # fit
            try:
                params, message, success = exp_fit(params, pec, expdata)
                if success:
                    out.print(f'\nPEC fit to exp. levels done: {message}')
                else:
                    self.print_message(f'ERROR: PEC fit to exp. levels FAILED: {message}', out)
                    return
            except BaseException as ex: # pylint: disable = W0718
                self.print_message(f'ERROR: failed to run "exp_fit" function: {str(ex)}\n', out)
                return

            # print final results
            out.print('\nFit results')
            try:
                levels = Levels('an', params)
            except BaseException as ex: # pylint: disable = W0718
                self.print_message(f'ERROR: failed to run "vr_solver" function: {str(ex)}\n', out)
                return
            levels.print_with_expdata(out, expdata)
            print_pecs(out, pec, params)
            out.print('\nFitted parameters\n')
            params.print_pec_params(out)

        #---
        out.close()
        self.print_message(f'SUCCESS! See "{fname}" for results\n')

        # back to normal stdout
        #sys.stdout = sys.__stdout__
        #out.close()
