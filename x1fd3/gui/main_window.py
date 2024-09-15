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
        self.mode = tk.StringVar()

        self.root.title('x1fd3')
        self.root.resizable(False, False)

        # mode selector
        ttk.Label(
            text = 'Select runtype mode',
            font = ('bold', 16)
        ).grid(
            row = 0,
            column = 0
            #columnspan = 4
        )

        ttk.Separator(
            orient = 'horizontal'
        ).grid(
            row = 1,
            column = 0
            #columnspan = 4,
            #sticky = 'ew'
        )

        ttk.Button(
            text = 'Point-wise PEC approximation with analytic function (EMO)',
            #value = 'PecApprox',
            #variable = self.mode,
            command = lambda: self.select_mode('PecApprox')
        ).grid(
            row = 2,
            column = 0
            #sticky = 'w'
        )

        ttk.Button(
            text = 'Vib.-rot. levels calculation with point-wise PEC',
            #value = 'LevelsPW',
            #variable = self.mode,
            command = lambda: self.select_mode('LevelsPW')
        ).grid(
            row = 3,
            column = 0
            #sticky = 'w'
        )


        ttk.Button(
            text = 'Vib.-rot. levels calculation with analytic PEC (EMO)',
            #value = 'LevelsAn',
            #variable = self.mode,
            command = lambda: self.select_mode('LevelsAn')
        ).grid(
            row = 4,
            column = 0
            #sticky = 'w'
        )

        ttk.Button(
            text = 'Vib.-rot. spectrum calculation with point-wise PEC',
            #value = 'SpectrumPW',
            #variable = self.mode,
            command = lambda: self.select_mode('SpectrumPW')
        ).grid(
            row = 5,
            column = 0
            #sticky = 'w'
        )


        ttk.Button(
            text = 'Vib.-rot. spectrum calculation with analytic PEC (EMO)',
            #value = 'SpectrumAn',
            #variable = self.mode,
            command = lambda: self.select_mode('SpectrumAn')
        ).grid(
            row = 6,
            column = 0
            #sticky = 'w'
        )

        ttk.Button(
            text = 'Fit PEC to reproduce experimental vib.-rot. levels',
            #value = 'FitExp',
            #variable = self.mode,
            command = lambda: self.select_mode('FitExp')
        ).grid(
            row = 7,
            column = 0
            #sticky = 'w'
        )

    def select_mode(
        self,
        mode: str
    ) -> None:
        '''
        draw sub window for calculation
        '''
        CalcWindow(self.root, mode)