import tkinter as tk
from tkinter import ttk

from .calc_window import CalcWindow

class MainWindow:
    '''
    class to draw main window
    '''
    def __init__(
        self
    ) -> None:
        '''
        draw buttons for mode selection
        '''
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
            'PecApprox': 'Point-wise PEC approximation with analytic function (EMO)',
            'LevelsPW': 'Vib.-rot. levels calculation with point-wise PEC',
            'LevelsAn': 'Vib.-rot. levels calculation with analytic PEC (EMO)',
            'SpectrumPW': 'Vib.-rot. spectrum calculation with point-wise PEC',
            'SpectrumAn': 'Vib.-rot. spectrum calculation with analytic PEC (EMO)',
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

    def select_mode(
        self
    ) -> None:
        '''
        draw sub window for calculation
        '''
        CalcWindow(self.root, self.mode.get())
        self.mode.set('')
