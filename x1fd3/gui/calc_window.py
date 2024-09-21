import traceback
from os.path import isfile, getsize, relpath
import tkinter as tk
from tkinter import filedialog
from tkinter import ttk

from x1fd3.base.p_w_curve import PWCurve
from x1fd3.base.parameters import Parameters
from x1fd3.base.levels import Levels
from x1fd3.base.matrix_elements import MatrixElements
from x1fd3.base.logger import Logger
from x1fd3.base.exp_data import ExpData
from x1fd3.base.print_input import print_input_file
from x1fd3.base.fit import Fit


class CalcWindow:
    '''
    sub window for calculation
    '''
    def __init__(
        self,
        main_root,
        mode: str
    ) -> None:
        '''
        draw stuff, mode dependent
        '''
        self.root = tk.Toplevel(main_root)
        self.root.title(mode)
        self.root.resizable(False, False)
        self.root.columnconfigure(0, minsize = 600)

        self.mode = mode

        # input files
        ttk.Label(
            self.root,
            text = 'Select input files',
            font = ('bold', 16)
        ).grid(
            row = 100,
            column = 0,
            columnspan = 4
        )

        ttk.Separator(
            self.root,
            orient = 'horizontal'
        ).grid(
            row = 101,
            column = 0,
            columnspan = 4,
            sticky = 'ew'
        )

        # PW pec
        if mode in [
            'PecApprox',
            'LevelsPW',
            'SpectrumPW',
            'FitExp'
        ]:
            tk.Label(
                self.root,
                text = 'Point-wise PEC, example: input/pw_pec.txt'
            ).grid(
                row = 102,
                column = 0,
                sticky = 'e'
            )

            self.file_pw_pec = ttk.Entry(
                self.root,
                width = 110,
            )
            self.file_pw_pec.grid(
                row = 102,
                column = 1
            )

            self.open_pw_pec = ttk.Button(
                self.root,
                text = 'Open a file',
                command = lambda: self.select_file(self.file_pw_pec)
            )
            self.open_pw_pec.grid(
                row = 102,
                column = 2
            )

        # VR levels calc params
        if mode in [
            'LevelsPW',
            'LevelsAn'
        ]:

            tk.Label(
                self.root,
                text = 'Parameters for vib.-rot. levels calculation, example: input/params_levels.txt'
            ).grid(
                row = 103,
                column = 0,
                sticky = 'e'
            )

            self.file_lev_calc = ttk.Entry(
                self.root,
                width = 110
            )
            self.file_lev_calc.grid(
                row = 103,
                column = 1
            )

            self.open_lev_calc = ttk.Button(
                self.root,
                text = 'Open a file',
                command = lambda: self.select_file(self.file_lev_calc)
            )
            self.open_lev_calc.grid(
                row = 103,
                column = 2
            )

        # VR spectrum calc params
        if mode in [
            'SpectrumPW',
            'SpectrumAn'
        ]:

            tk.Label(
                self.root,
                text = 'Parameters for vib.-rot. spectrum calculation, example: input/params_spectrum.txt'
            ).grid(
                row = 104,
                column = 0,
                sticky = 'e'
            )

            self.file_sp_calc = ttk.Entry(
                self.root,
                width = 110
            )
            self.file_sp_calc.grid(
                row = 104,
                column = 1
            )

            self.open_sp_calc = ttk.Button(
                self.root,
                text = 'Open a file',
                command = lambda: self.select_file(self.file_sp_calc)
            )
            self.open_sp_calc.grid(
                row = 104,
                column = 2
            )

        # VR fit params
        if mode in [
            'FitExp'
        ]:

            tk.Label(
                self.root,
                text = 'Parameters for vib.-rot. levels calculation, example: input/params_fit.txt'
            ).grid(
                row = 105,
                column = 0,
                sticky = 'e'
            )

            self.file_fit_calc = ttk.Entry(
                self.root,
                width = 110
            )
            self.file_fit_calc.grid(
                row = 105,
                column = 1
            )

            self.open_fit_calc = ttk.Button(
                self.root,
                text = 'Open a file',
                command = lambda: self.select_file(self.file_fit_calc)
            )
            self.open_fit_calc.grid(
                row = 105,
                column = 2
            )

        # init params
        if mode in [
            'PecApprox'
        ]:
            tk.Label(
                self.root,
                text = 'Initial parameters for PEC approxomation, example: input/init_emo.txt'
            ).grid(
                row = 106,
                column = 0,
                sticky = 'e'
            )

            self.file_init_params = ttk.Entry(
                self.root,
                width = 110
            )
            self.file_init_params.grid(
                row = 106,
                column = 1
            )

            self.open_init_params = ttk.Button(
                self.root,
                text = 'Open a file',
                command = lambda: self.select_file(self.file_init_params)
            )
            self.open_init_params.grid(
                row = 106,
                column = 2
            )

        # fitted params
        if mode in [
            'LevelsAn',
            'SpectrumAn',
            'FitExp'
        ]:
            tk.Label(
                self.root,
                text = 'Fitted PEC parameters for levels/spectrum calculation, example: input/fitted_emo.txt'
            ).grid(
                row = 107,
                column = 0,
                sticky = 'e'
            )

            self.file_fitted_params = ttk.Entry(
                self.root,
                width = 110
            )
            self.file_fitted_params.grid(
                row = 107,
                column = 1
            )

            self.open_fitted_params = ttk.Button(
                self.root,
                text = 'Open a file',
                command = lambda: self.select_file(self.file_fitted_params)
            )
            self.open_fitted_params.grid(
                row = 107,
                column = 2
            )

        # dipole
        if mode in [
            'SpectrumPW',
            'SpectrumAn'
        ]:
            tk.Label(
                self.root,
                text = 'Point-wise dipole moment, example: input/pw_dm.txt'
            ).grid(
                row = 108,
                column = 0,
                sticky = 'e'
            )

            self.file_pw_dip = ttk.Entry(
                self.root,
                width = 110
            )
            self.file_pw_dip.grid(
                row = 108,
                column = 1
            )

            self.open_pw_dip = ttk.Button(
                self.root,
                text = 'Open a file',
                command = lambda: self.select_file(self.file_pw_dip)
            )
            self.open_pw_dip.grid(
                row = 108,
                column = 2
            )

        # exp data
        if mode in [
            'FitExp'
        ]:
            tk.Label(
                self.root,
                text = 'Experimental vib.-rot. levels, example: input/exp_levels.txt'
            ).grid(
                row = 109,
                column = 0,
                sticky = 'e'
            )

            self.file_exp = ttk.Entry(
                self.root,
                width = 110
            )
            self.file_exp.grid(
                row = 109,
                column = 1
            )

            self.open_exp = ttk.Button(
                self.root,
                text = 'Open a file',
                command = lambda: self.select_file(self.file_exp)
            )
            self.open_exp.grid(
                row = 109,
                column = 2
            )

        # out file
        ttk.Label(
            self.root,
            text = 'Select out file',
            font = ('bold', 16)
        ).grid(
            row = 110,
            column = 0,
            columnspan = 4
        )

        ttk.Separator(
            self.root,
            orient = 'horizontal'
        ).grid(
            row = 111,
            column = 0,
            columnspan = 4,
            sticky = 'ew'
        )

        tk.Label(
            self.root,
            text = 'Output file:'
        ).grid(
            row = 112,
            column = 0,
            sticky = 'e'
        )

        self.file_out = ttk.Entry(
            self.root,
            width = 110
        )
        self.file_out.grid(
            row = 112,
            column = 1
        )

        self.open_out = ttk.Button(
            self.root,
            text = 'Open a file',
            command = lambda: self.select_file(self.file_out)
        )
        self.open_out.grid(
            row = 112,
            column = 2
        )

        # window for messages
        self.vscroll = tk.Scrollbar(
            self.root,
            orient = 'vertical'
        )
        self.vscroll.grid(
            row = 113,
            column = 3,
            sticky = tk.N + tk.S
        )

        self.message_window = tk.Text(
            self.root,
            width = 160,
            height = 20,
            state = 'disabled',
            yscrollcommand = self.vscroll.set
        )
        self.message_window.grid(
            row = 113,
            column = 0,
            columnspan = 3,
            sticky = tk.W + tk.E
        )

        # run
        ttk.Style().configure('my.TButton', font = ('bold', 16), foreground = 'red')

        ttk.Button(
            self.root,
            text = 'RUN',
            width = 50,
            style = 'my.TButton',
            command = self.run_calc
        ).grid(
            row = 114,
            column = 0,
            columnspan = 4
        )

        # lock main
        self.root.transient(main_root)
        self.root.grab_set()
        main_root.wait_window(self.root)


    def print_message(
        self,
        string: str,
        out: Logger
    ) -> None:
        '''
        print to window and to out file if opened
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
            fname = relpath(fname)

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
                self.print_message(f'ERROR: non-empty out file "{fname}" already exists\n', Logger())
                return
        else:
            self.print_message('ERROR: out file not specified\n', Logger())
            return

        out = Logger(fname, False)

        # PecApprox mode
        if self.mode == 'PecApprox':

            f_pw_pec = self.file_pw_pec.get()
            f_init_par = self.file_init_params.get()

            # print input
            try:
                out.print('* Point-wise PEC *')
                print_input_file(out, f_pw_pec)
            except BaseException: # pylint: disable = W0718
                self.print_message('ERROR: failed to read input file with point-wise PEC', out)
                self.print_message(traceback.format_exc(), out)
                return

            try:
                out.print('* Init PEC parameters *')
                print_input_file(out, f_init_par)
            except BaseException: # pylint: disable = W0718
                self.print_message('ERROR: failed to read input file with initial parameters for PEC approximation', out)
                self.print_message(traceback.format_exc(), out)
                return

            # read files
            try:
                pec = PWCurve(f_pw_pec)
            except BaseException: # pylint: disable = W0718
                self.print_message('ERROR: failed to read point-wise PEC', out)
                self.print_message(traceback.format_exc(), out)
                return

            try:
                params = Parameters()
                params.read_pec_params(f_init_par)
            except BaseException: # pylint: disable = W0718
                self.print_message('ERROR: failed to read initial PEC parameters', out)
                self.print_message(traceback.format_exc(), out)
                return

            out.print('=== Point-wise PEC approximation ===\n')

            # fit
            try:
                Fit(pec, params).fit_n_print(out)
            except BaseException: # pylint: disable = W0718
                self.print_message('ERROR: fit failed', out)
                self.print_message(traceback.format_exc(), out)
                return

        # LevelsPW mode
        if self.mode == 'LevelsPW':

            f_vr_par = self.file_lev_calc.get()
            f_pw_pec = self.file_pw_pec.get()

            # print input
            try:
                out.print('* Parameter for vib.-rot. levels calculation *')
                print_input_file(out, f_vr_par)
            except BaseException: # pylint: disable = W0718
                self.print_message('ERROR: failed to read input file with parameter for vib.-rot. levels calculation', out)
                self.print_message(traceback.format_exc(), out)
                return

            try:
                out.print('* Point-wise PEC *')
                print_input_file(out, f_pw_pec)
            except BaseException: # pylint: disable = W0718
                self.print_message('ERROR: failed to read input file with point-wise PEC', out)
                self.print_message(traceback.format_exc(), out)
                return

            # read files
            try:
                pec = PWCurve(f_pw_pec)
            except BaseException: # pylint: disable = W0718
                self.print_message('ERROR: failed to read point-wise PEC', out)
                self.print_message(traceback.format_exc(), out)
                return

            try:
                params = Parameters()
                params.read_vr_calc_params(f_vr_par, 'ENERGY')
            except BaseException: # pylint: disable = W0718
                self.print_message('ERROR: failed to read parameter for vib.-rot. levels calculation', out)
                self.print_message(traceback.format_exc(), out)
                return

            # calc and print vr levels
            try:
                Levels('pw', params, pec).print(out)
            except BaseException: # pylint: disable = W0718
                self.print_message('ERROR: levels calculation failed', out)
                self.print_message(traceback.format_exc(), out)
                return


        # LevelsAn mode
        if self.mode == 'LevelsAn':

            f_vr_par = self.file_lev_calc.get()
            f_fit_par = self.file_fitted_params.get()

            # print input
            try:
                out.print('* Parameter for vib.-rot. levels calculation *')
                print_input_file(out, f_vr_par)
            except BaseException: # pylint: disable = W0718
                self.print_message('ERROR: failed to read input file with parameter for vib.-rot. levels calculation', out)
                self.print_message(traceback.format_exc(), out)
                return

            try:
                out.print('* Fitted PEC parameters *')
                print_input_file(out, f_fit_par)
            except BaseException: # pylint: disable = W0718
                self.print_message('ERROR: failed to read input file with fitted PEC parameters', out)
                self.print_message(traceback.format_exc(), out)
                return

            # read files
            try:
                params = Parameters()
                params.read_vr_calc_params(f_vr_par, 'ENERGY')
            except BaseException: # pylint: disable = W0718
                self.print_message('ERROR: failed to read parameter for vib.-rot. levels calculation', out)
                self.print_message(traceback.format_exc(), out)
                return

            try:
                params.read_pec_params(f_fit_par)
            except BaseException: # pylint: disable = W0718
                self.print_message('ERROR: failed to read fitted PEC parameters', out)
                self.print_message(traceback.format_exc(), out)
                return

            # calc and print vr levels
            try:
                Levels('an', params).print(out)
            except BaseException: # pylint: disable = W0718
                self.print_message('ERROR: levels calculation failed', out)
                self.print_message(traceback.format_exc(), out)
                return

        # SpectrumPW mode
        if self.mode == 'SpectrumPW':

            f_vr_par = self.file_sp_calc.get()
            f_pw_pec = self.file_pw_pec.get()
            f_pw_dm = self.file_pw_dip.get()

            # print input
            try:
                out.print('* Parameters for vib.-rot. spectrum calculation *')
                print_input_file(out, f_vr_par)
            except BaseException: # pylint: disable = W0718
                self.print_message('ERROR: failed to read input file with parameter for vib.-rot. spectrum calculation', out)
                self.print_message(traceback.format_exc(), out)
                return

            try:
                out.print('* Point-wise PEC *')
                print_input_file(out, f_pw_pec)
            except BaseException: # pylint: disable = W0718
                self.print_message('ERROR: failed to read input file with point-wise PEC', out)
                self.print_message(traceback.format_exc(), out)
                return

            try:
                out.print('* Point-wise dipole moment *')
                print_input_file(out, f_pw_dm)
            except BaseException: # pylint: disable = W0718
                self.print_message('ERROR: failed to read input file with point-wise dipole moment', out)
                self.print_message(traceback.format_exc(), out)
                return

            # read files
            try:
                pec = PWCurve(f_pw_pec)
            except BaseException: # pylint: disable = W0718
                self.print_message('ERROR: failed to read point-wise PEC', out)
                self.print_message(traceback.format_exc(), out)
                return

            try:
                dm = PWCurve(f_pw_dm)
            except BaseException: # pylint: disable = W0718
                self.print_message('ERROR: failed to read point-wise dipole moment', out)
                self.print_message(traceback.format_exc(), out)
                return

            try:
                params = Parameters()
                params.read_vr_calc_params(f_vr_par, 'SPECTRUM')
            except BaseException: # pylint: disable = W0718
                self.print_message('ERROR: failed to read parameter for vib.-rot. spectrum calculation', out)
                self.print_message(traceback.format_exc(), out)
                return

            # calc vr levels
            try:
                levels = Levels('pw', params, pec)
            except BaseException: # pylint: disable = W0718
                self.print_message('ERROR: failed to run "vr_solver" function', out)
                self.print_message(traceback.format_exc(), out)
                return

            # calc and print integrals
            try:
                MatrixElements(params, levels, dm).print(out)
            except BaseException: # pylint: disable = W0718
                self.print_message('ERROR: matrix elements calculation failed', out)
                self.print_message(traceback.format_exc(), out)
                return

        # SpectrumAn mode
        if self.mode == 'SpectrumAn':

            f_vr_par = self.file_sp_calc.get()
            f_fit_par = self.file_fitted_params.get()
            f_pw_dm = self.file_pw_dip.get()

            # print input
            try:
                out.print('* Parameters for vib.-rot. spectrum calculation *')
                print_input_file(out, f_vr_par)
            except BaseException: # pylint: disable = W0718
                self.print_message('ERROR: failed to read input file with parameter for vib.-rot. spectrum calculation', out)
                self.print_message(traceback.format_exc(), out)
                return

            try:
                out.print('* Fitted PEC parameters *')
                print_input_file(out, f_fit_par)
            except BaseException: # pylint: disable = W0718
                self.print_message('ERROR: failed to read input file with fitted PEC parameters', out)
                self.print_message(traceback.format_exc(), out)
                return

            try:
                out.print('* Point-wise dipole moment *')
                print_input_file(out, f_pw_dm)
            except BaseException: # pylint: disable = W0718
                self.print_message('ERROR: failed to read input file with point-wise dipole moment', out)
                self.print_message(traceback.format_exc(), out)
                return

            # read files
            try:
                params = Parameters()
                params.read_vr_calc_params(f_vr_par, 'SPECTRUM')
            except BaseException: # pylint: disable = W0718
                self.print_message('ERROR: failed to read parameter for vib.-rot. spectrum calculation', out)
                self.print_message(traceback.format_exc(), out)
                return

            try:
                params.read_pec_params(f_fit_par)
            except BaseException: # pylint: disable = W0718
                self.print_message('ERROR: failed to read fitted PEC parameters', out)
                self.print_message(traceback.format_exc(), out)
                return

            try:
                dm = PWCurve(f_pw_dm)
            except BaseException: # pylint: disable = W0718
                self.print_message('ERROR: failed to read point-wise dipole moment', out)
                self.print_message(traceback.format_exc(), out)
                return

            # calc vr levels
            try:
                levels = Levels('an', params)
            except BaseException: # pylint: disable = W0718
                self.print_message('ERROR: failed to run "vr_solver" function', out)
                self.print_message(traceback.format_exc(), out)
                return

            # calc and print integrals
            try:
                MatrixElements(params, levels, dm).print(out)
            except BaseException: # pylint: disable = W0718
                self.print_message('ERROR: matrix elements calculation failed', out)
                self.print_message(traceback.format_exc(), out)
                return

        # FitExp
        if self.mode == 'FitExp':

            f_vr_par = self.file_fit_calc.get()
            f_fit_par = self.file_fitted_params.get()
            f_pw_pec = self.file_pw_pec.get()
            f_epx_lev = self.file_exp.get()

            # print input
            try:
                out.print('* Parameters for PEC fit to exp. levels *')
                print_input_file(out, f_vr_par)
            except BaseException: # pylint: disable = W0718
                self.print_message('ERROR: failed to read input file with parameter for PEC fit to exp. levels', out)
                self.print_message(traceback.format_exc(), out)
                return

            try:
                out.print('* Fitted PEC parameters *')
                print_input_file(out, f_fit_par)
            except BaseException: # pylint: disable = W0718
                self.print_message('ERROR: failed to read input file with fitted PEC parameters', out)
                self.print_message(traceback.format_exc(), out)
                return

            try:
                out.print('* Point-wise PEC *')
                print_input_file(out, f_pw_pec)
            except BaseException: # pylint: disable = W0718
                self.print_message('ERROR: failed to read input file with point-wise PEC', out)
                self.print_message(traceback.format_exc(), out)
                return

            try:
                out.print('* Exp. levels *')
                print_input_file(out, f_epx_lev)
            except BaseException: # pylint: disable = W0718
                self.print_message('ERROR: failed to read input file with exp. vib.-rot. levels', out)
                self.print_message(traceback.format_exc(), out)
                return

            # read files
            try:
                pec = PWCurve(f_pw_pec)
            except BaseException: # pylint: disable = W0718
                self.print_message('ERROR: failed to read point-wise PEC', out)
                self.print_message(traceback.format_exc(), out)
                return

            try:
                params = Parameters()
                params.read_vr_calc_params(f_vr_par, 'FIT')
            except BaseException: # pylint: disable = W0718
                self.print_message('ERROR: failed to read parameter for PEC fit to exp. levels', out)
                self.print_message(traceback.format_exc(), out)
                return

            try:
                params.read_pec_params(f_fit_par)
            except BaseException: # pylint: disable = W0718
                self.print_message('ERROR: failed to read fitted PEC parameters', out)
                self.print_message(traceback.format_exc(), out)
                return

            try:
                expdata = ExpData(f_epx_lev)
            except BaseException: # pylint: disable = W0718
                self.print_message('ERROR: failed to read exp. vib.-rot. levels', out)
                self.print_message(traceback.format_exc(), out)
                return

            params['jmax'] = max(expdata.energy.keys())

            out.print('=== Fit PEC to reproduce experimental data ===\n')

            # fit
            try:
                Fit(pec, params, expdata).fit_n_print(out)
            except BaseException: # pylint: disable = W0718
                self.print_message('ERROR: fit failed', out)
                self.print_message(traceback.format_exc(), out)
                return

        out.close()
        self.print_message(f'SUCCESS! See "{fname}" for results\n', Logger())
