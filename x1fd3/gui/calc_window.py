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
        main_root:tk.Tk,
        mode:str,
    ) -> None:
        '''
        draw stuff, mode dependent
        '''
        self.root = tk.Toplevel(main_root)
        self.root.title(mode)
        self.root.resizable(False, False)
        #self.root.columnconfigure(0, minsize=600)

        self.mode = mode

        # first row
        row = 1

        # input files
        ttk.Label(
            self.root,
            text='Select input files',
            font=('bold', 16)
        ).grid(
            row=row,
            column=0,
            columnspan=4
        )

        row += 1

        ttk.Separator(
            self.root,
            orient='horizontal'
        ).grid(
            row=row,
            column=0,
            columnspan=4,
            sticky='ew'
        )

        row += 1

        # VR levels calc params
        if mode in [
            'LevelsPW',
            'LevelsAn'
        ]:

            tk.Label(
                self.root,
                text='Parameters levels calculation, example: input/params_levels.txt'
            ).grid(
                row=row,
                column=0,
                sticky='e'
            )

            self.file_lev_calc = ttk.Entry(
                self.root,
                width=50
            )
            self.file_lev_calc.grid(
                row=row,
                column=1
            )

            self.open_lev_calc = ttk.Button(
                self.root,
                text='Open a file',
                command=lambda: self.select_file(self.file_lev_calc)
            )
            self.open_lev_calc.grid(
                row=row,
                column=2
            )

            row += 1

        # VR spectrum calc params
        if mode in [
            'SpectrumPW',
            'SpectrumAn'
        ]:

            tk.Label(
                self.root,
                text='Parameters for spectrum calculation, example: input/params_spectrum.txt'
            ).grid(
                row=row,
                column=0,
                sticky='e'
            )

            self.file_sp_calc = ttk.Entry(
                self.root,
                width=50
            )
            self.file_sp_calc.grid(
                row=row,
                column=1
            )

            self.open_sp_calc = ttk.Button(
                self.root,
                text='Open a file',
                command=lambda: self.select_file(self.file_sp_calc)
            )
            self.open_sp_calc.grid(
                row=row,
                column=2
            )

            row += 1

        # VR fit params
        if mode in [
            'FitExp'
        ]:

            tk.Label(
                self.root,
                text='Parameters for fit procedure, example: input/params_fit.txt'
            ).grid(
                row=row,
                column=0,
                sticky='e'
            )

            self.file_fit_calc = ttk.Entry(
                self.root,
                width=50
            )
            self.file_fit_calc.grid(
                row=row,
                column=1
            )

            self.open_fit_calc = ttk.Button(
                self.root,
                text='Open a file',
                command=lambda: self.select_file(self.file_fit_calc)
            )
            self.open_fit_calc.grid(
                row=row,
                column=2
            )

            row += 1

        # init params
        if mode in [
            'PecApprox'
        ]:
            tk.Label(
                self.root,
                text='Initial PEC parameters, example: input/init_emo.txt'
            ).grid(
                row=row,
                column=0,
                sticky='e'
            )

            self.file_init_params = ttk.Entry(
                self.root,
                width=50
            )
            self.file_init_params.grid(
                row=row,
                column=1
            )

            self.open_init_params = ttk.Button(
                self.root,
                text='Open a file',
                command=lambda: self.select_file(self.file_init_params)
            )
            self.open_init_params.grid(
                row=row,
                column=2
            )

            row += 1

        # fitted params
        if mode in [
            'LevelsAn',
            'SpectrumAn',
            'FitExp'
        ]:
            tk.Label(
                self.root,
                text='Fitted PEC parameters, example: input/fitted_emo.txt'
            ).grid(
                row=row,
                column=0,
                sticky='e'
            )

            self.file_fitted_params = ttk.Entry(
                self.root,
                width=50
            )
            self.file_fitted_params.grid(
                row=row,
                column=1
            )

            self.open_fitted_params = ttk.Button(
                self.root,
                text='Open a file',
                command=lambda: self.select_file(self.file_fitted_params)
            )
            self.open_fitted_params.grid(
                row=row,
                column=2
            )

            row += 1

        # PW pec
        if mode in [
            'PecApprox',
            'LevelsPW',
            'SpectrumPW',
            'FitExp'
        ]:
            tk.Label(
                self.root,
                text='Point-wise PEC, example: input/pw_pec.txt'
            ).grid(
                row=row,
                column=0,
                sticky='e'
            )

            self.file_pw_pec = ttk.Entry(
                self.root,
                width=50,
            )
            self.file_pw_pec.grid(
                row=row,
                column=1
            )

            self.open_pw_pec = ttk.Button(
                self.root,
                text='Open a file',
                command=lambda: self.select_file(self.file_pw_pec)
            )
            self.open_pw_pec.grid(
                row=row,
                column=2
            )

            row += 1

        # PW dipole
        if mode in [
            'SpectrumPW',
            'SpectrumAn'
        ]:
            tk.Label(
                self.root,
                text='Point-wise dipole moment, example: input/pw_dm.txt'
            ).grid(
                row=row,
                column=0,
                sticky='e'
            )

            self.file_pw_dip = ttk.Entry(
                self.root,
                width=50
            )
            self.file_pw_dip.grid(
                row=row,
                column=1
            )

            self.open_pw_dip = ttk.Button(
                self.root,
                text='Open a file',
                command=lambda: self.select_file(self.file_pw_dip)
            )
            self.open_pw_dip.grid(
                row=row,
                column=2
            )

            row += 1

        # exp data
        if mode in [
            'FitExp'
        ]:
            tk.Label(
                self.root,
                text='Experimental vib.-rot. levels, example: input/exp_levels.txt'
            ).grid(
                row=row,
                column=0,
                sticky='e'
            )

            self.file_exp = ttk.Entry(
                self.root,
                width=50
            )
            self.file_exp.grid(
                row=row,
                column=1
            )

            self.open_exp = ttk.Button(
                self.root,
                text='Open a file',
                command=lambda: self.select_file(self.file_exp)
            )
            self.open_exp.grid(
                row=row,
                column=2
            )

            row += 1

        # out file
        ttk.Label(
            self.root,
            text='Select out file',
            font=('bold', 16)
        ).grid(
            row=row,
            column=0,
            columnspan=4
        )

        row += 1

        ttk.Separator(
            self.root,
            orient='horizontal'
        ).grid(
            row=row,
            column=0,
            columnspan=4,
            sticky='ew'
        )

        row += 1

        tk.Label(
            self.root,
            text='Output file:'
        ).grid(
            row=row,
            column=0,
            sticky='e'
        )

        self.file_out=ttk.Entry(
            self.root,
            width=50
        )
        self.file_out.grid(
            row=row,
            column=1
        )

        self.open_out = ttk.Button(
            self.root,
            text='Open a file',
            command=lambda: self.select_file(self.file_out)
        )
        self.open_out.grid(
            row=row,
            column=2
        )

        row += 1

        # window for messages
        self.vscroll = tk.Scrollbar(
            self.root,
            orient='vertical'
        )
        self.vscroll.grid(
            row=row,
            column=3,
            sticky=tk.N + tk.S
        )

        self.message_window = tk.Text(
            self.root,
            #width=100,
            height=20,
            state='disabled',
            yscrollcommand=self.vscroll.set
        )
        self.message_window.grid(
            row=row,
            column=0,
            columnspan=3,
            sticky=tk.W + tk.E
        )

        row += 1

        # run
        ttk.Style().configure('my.TButton', font=('bold', 16), foreground='red')

        ttk.Button(
            self.root,
            text='RUN',
            width=50,
            style='my.TButton',
            command=self.run_calc
        ).grid(
            row=row,
            column=0,
            columnspan=4
        )

        # lock main
        self.root.transient(main_root)
        self.root.grab_set()
        main_root.wait_window(self.root)

    def print_message(
        self,
        string:str,
        out:Logger
    ) -> None:
        '''
        print to window and to out file if opened
        '''
        self.message_window.configure(state='normal')
        self.message_window.insert('end', string)
        self.message_window.configure(state='disabled')

        if out.fname:
            out.print(string)

    def select_file(
            self,
            obj:ttk.Entry
        ) -> None:
        '''
        function for tk open file dialog
        '''
        filetypes = (
            ('text files', '*.txt'),
            ('All files', '*.*')
        )

        fname = filedialog.askopenfilename(
            title='Open a file',
            filetypes=filetypes
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
        # input files for mode
        if self.mode == 'PecApprox':
            input_files = [
                self.file_init_params.get(),
                self.file_pw_pec.get()
            ]
        elif self.mode == 'LevelsPW':
            input_files = [
                self.file_lev_calc.get(),
                self.file_pw_pec.get()
            ]
        elif self.mode == 'LevelsAn':
            input_files = [
                self.file_lev_calc.get(),
                self.file_fitted_params.get()
            ]
        elif self.mode == 'SpectrumPW':
            input_files = [
                self.file_sp_calc.get(),
                self.file_pw_pec.get(),
                self.file_pw_dip.get()
            ]
        elif self.mode == 'SpectrumAn':
            input_files = [
                self.file_sp_calc.get(),
                self.file_fitted_params.get(),
                self.file_pw_dip.get(),
            ]
        elif self.mode == 'FitExp':
            input_files = [
                self.file_fit_calc.get(),
                self.file_fitted_params.get(),
                self.file_pw_pec.get(),
                self.file_exp.get()
            ]
        else:
            return

        # check input files
        if not all(input_files):
            self.print_message('RuntimeError: one or more input files not specified\n', Logger())
            return

        # set out if possible
        fname = self.file_out.get()
        if not fname:
            self.print_message('RuntimeError: out file not specified\n', Logger())
            return
        if isfile(fname) and getsize(fname) > 0:
            self.print_message(f'RuntimeError: non-empty out file "{fname}" already exists\n', Logger())
            return
        out = Logger(fname, False)

        # run calc for mode
        try:
            if self.mode == 'PecApprox':
                DriverPecApprox(input_files, out).run()
            elif self.mode == 'LevelsPW':
                DriverLevelsPW(input_files, out).run()
            elif self.mode == 'LevelsAn':
                DriverLevelsAn(input_files, out).run()
            elif self.mode == 'SpectrumPW':
                DriverSpectrumPW(input_files, out).run()
            elif self.mode == 'SpectrumAn':
                DriverSpectrumAn(input_files, out).run()
            elif self.mode == 'FitExp':
                DriverFitExp(input_files, out).run()
            else:
                return
        except BaseException as ex: # pylint: disable = W0718
            self.print_message(f'RuntimeError: {ex}\n', Logger())
            out.print(traceback.format_exc())
            return

        out.close()
        self.print_message(f'SUCCESS! See "{out.fname}" for results\n', Logger())
