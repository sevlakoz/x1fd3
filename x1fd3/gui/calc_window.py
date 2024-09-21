import traceback
from os.path import isfile, \
                    getsize, \
                    relpath
import tkinter as tk
from tkinter import filedialog
from tkinter import ttk

from x1fd3.base import Logger
from x1fd3.cli import DriverPecApprox, \
                      DriverLevelsPW, \
                      DriverLevelsAn, \
                      DriverSpectrumPW, \
                      DriverSpectrumAn, \
                      DriverFitExp

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
                self.print_message(f'RuntimeError: non-empty out file "{fname}" already exists\n', Logger())
                return
        else:
            self.print_message('RuntimeError: out file not specified\n', Logger())
            return

        out = Logger(fname, False)

        # PecApprox mode
        if self.mode == 'PecApprox':

            input_files = [
                self.file_pw_pec.get(),
                self.file_init_params.get()
            ]

            try:
                DriverPecApprox(self.mode, input_files, out).run()
            except BaseException as ex: # pylint: disable = W0718
                self.print_message(f'RuntimeError: {ex}\n', Logger())
                out.print(traceback.format_exc())
                return

        # LevelsPW mode
        if self.mode == 'LevelsPW':

            input_files = [
                self.file_lev_calc.get(),
                self.file_pw_pec.get()
            ]

            try:
                DriverLevelsPW(self.mode, input_files, out).run()
            except BaseException as ex: # pylint: disable = W0718
                self.print_message(f'RuntimeError: {ex}\n', Logger())
                out.print(traceback.format_exc())
                return

        # LevelsAn mode
        if self.mode == 'LevelsAn':

            input_files = [
                self.file_lev_calc.get(),
                self.file_fitted_params.get()
            ]

            try:
                DriverLevelsAn(self.mode, input_files, out).run()
            except BaseException as ex: # pylint: disable = W0718
                self.print_message(f'RuntimeError: {ex}\n', Logger())
                out.print(traceback.format_exc())
                return

        # SpectrumPW mode
        if self.mode == 'SpectrumPW':

            input_files = [
                self.file_sp_calc.get(),
                self.file_pw_pec.get(),
                self.file_pw_dip.get()
            ]

            try:
                DriverSpectrumPW(self.mode, input_files, out).run()
            except BaseException as ex: # pylint: disable = W0718
                self.print_message(f'RuntimeError: {ex}\n', Logger())
                out.print(traceback.format_exc())
                return

        # SpectrumAn mode
        if self.mode == 'SpectrumAn':

            input_files = [
                self.file_sp_calc.get(),
                self.file_fitted_params.get(),
                self.file_pw_dip.get(),
            ]

            try:
                DriverSpectrumAn(self.mode, input_files, out).run()
            except BaseException as ex: # pylint: disable = W0718
                self.print_message(f'RuntimeError: {ex}\n', Logger())
                out.print(traceback.format_exc())
                return

        # FitExp
        if self.mode == 'FitExp':

            input_files = [
                self.file_fit_calc.get(),
                self.file_fitted_params.get(),
                self.file_pw_pec.get(),
                self.file_exp.get()
            ]

            try:
                DriverFitExp(self.mode, input_files, out).run()
            except BaseException as ex: # pylint: disable = W0718
                self.print_message(f'RuntimeError: {ex}\n', Logger())
                out.print(traceback.format_exc())
                return

        out.close()
        self.print_message(f'SUCCESS! See "{fname}" for results\n', Logger())
