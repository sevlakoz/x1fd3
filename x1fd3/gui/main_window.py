import tkinter as tk
from tkinter import ttk

from .calc_window import CalcWindow

class MainWindow:
    '''
    class to draw main window
    '''
    def __init__(
        self,
        args: list[str]
    ) -> None:
        '''
        draw buttons for mode selection
        '''
        #self.input_files = input_files

        self.root = tk.Tk()

        self.root.title('x1fd3')
        self.root.resizable(False, False)

        self.mode = tk.StringVar()

        ttk.Label(
            text = 'Mode',
            font = ('bold', 16)
        ).grid(
            row = 0,
            column = 0,
            sticky = 'w'
        )

        ttk.Label(
            text = 'Description',
            font = ('bold', 16)
        ).grid(
            row = 0,
            column = 1,
            sticky = 'w'
        )

        ttk.Separator(
            orient = 'horizontal'
        ).grid(
            row = 1,
            column = 0,
            columnspan = 2,
            sticky = 'ew'
        )

        modes = {
            'PecApprox': 'Point-wise PEC approximation with analytic function',
            'LevelsPW': 'Vib.-rot. levels calculation with point-wise PEC',
            'LevelsAn': 'Vib.-rot. levels calculation with analytic PEC',
            'SpectrumPW': 'Vib.-rot. spectrum calculation with point-wise PEC',
            'SpectrumAn': 'Vib.-rot. spectrum calculation with analytic PEC',
            'FitExp': 'Fit PEC to reproduce experimental vib.-rot. levels'
        }

        ttk.Style().configure('my.TRadiobutton', font = ('bold'), foreground = 'red')

        row = 2
        for mode, descr in modes.items():
            ttk.Radiobutton(
                text = mode,
                style = 'my.TRadiobutton',
                value = mode,
                variable = self.mode,
                command = self.select_mode
            ).grid(
                row = row,
                column = 0,
                sticky = 'w'
            )

            tk.Label(
                text = descr
            ).grid(
                row = row,
                column = 1,
                sticky = 'w'
            )

            row += 1

        # autorun for test
        if len(args) > 3 and args[0] == 'autorun' and args[1] in modes:
            mode = args[1]
            input_files = tuple(args[2:])
            out_file = f'{mode}_GUI_autorun.log'
            CalcWindow(self.root, mode, True, input_files, out_file)
            self.root.destroy()

    def select_mode(
        self
    ) -> None:
        '''
        draw sub window for calculation
        '''
        CalcWindow(self.root, self.mode.get())
        self.mode.set('')
