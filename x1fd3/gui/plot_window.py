from os.path import relpath
import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
import numpy as np
import matplotlib.pyplot as plt

from x1fd3.base import PWCurve

class PlotWindow:
    '''
    window to select out file for visualization
    '''
    def __init__(
        self,
        main_root:tk.Tk,
        mode:str,
    ) -> None:
        '''
        draw base elements
        '''
        self.root = tk.Toplevel(main_root)
        self.root.title(mode)
        self.root.resizable(False, False)

        row = 1

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
            text='Output file, examples: test/*.ref'
        ).grid(
            row=row,
            column=0,
            sticky='e'
        )

        self.file_out = ttk.Entry(
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

        # draw
        ttk.Style().configure('my.TButton', font=('bold', 16), foreground='red')

        ttk.Button(
            self.root,
            text='DRAW',
            width=50,
            style='my.TButton',
            command=self.draw
        ).grid(
            row=row,
            column=0,
            columnspan=4
        )


        # lock main
        self.root.transient(main_root)
        self.root.grab_set()
        main_root.wait_window(self.root)

    def select_file(
            self,
            obj:ttk.Entry
        ) -> None:
        '''
        function for tk open file dialog
        '''
        filetypes = (
            ('Text files', '*.out'),
            ('Text files', '*.log'),
            ('Text files', '*.ref'),
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

    def print_message(
        self,
        string:str
    ) -> None:
        '''
        print to window
        '''
        self.message_window.configure(state='normal')
        self.message_window.insert('end', string)
        self.message_window.configure(state='disabled')

    def draw(
        self
    ) -> None:
        '''
        draw matplotlib plot for given out file
        '''
        fname = self.file_out.get()

        # read data
        try:
            data = open(fname, encoding='utf-8').readlines()
        except BaseException as ex: # pylint: disable = W0718
            self.print_message(f'Failed to open out file: {ex}\n')
            return

        # find mode
        try:
            mode = data[0].split()[1]
        except BaseException as ex: # pylint: disable = W0718
            self.print_message(f'Failed to extract mode from out: {ex}\n')
            return

        # draw plot
        try:
            if mode == 'PecApprox':
                start = data.index('Initial PEC\n') + 3
                stop = data.index('Initial parameters\n') - 1
                tmp = np.genfromtxt(data[start:stop]).T
                r_ab = tmp[0]
                u_ab = tmp[1]
                u_f = tmp[2]
                r_f = np.arange(r_ab[0], r_ab[-1], 0.001)
                u_fi = PWCurve(rvs=r_ab, cvs=u_f).spline(r_f)

                start = data.index('Fitted PEC\n') + 3
                stop = data.index('Fitted parameters\n') - 1
                tmp = np.genfromtxt(data[start:stop]).T
                u_f = tmp[2]
                u_ff = PWCurve(rvs=r_ab, cvs=u_f).spline(r_f)

                plt.figure(figsize=(10,5))
                plt.grid()
                plt.scatter(r_ab, u_ab, label='ab initio', c='black')
                plt.plot(r_f, u_fi, label='fit init', c='blue')
                plt.plot(r_f, u_ff, label='fit final', c='red')
                plt.legend()
                plt.xlabel(r'R, $\mathrm{\AA}$')
                plt.ylabel('U, cm${}^{-1}$')
                plt.show()

            elif mode == 'FitExp':
                start = data.index('Initial levels\n') + 3
                stop = data.index('Initial PEC\n') - 1
                tmp = np.genfromtxt(data[start:stop]).T
                e_exp = tmp[2]
                d_init = tmp[4]

                start = data.index('Fitted levels\n') + 3
                stop = data.index('Fitted PEC\n') - 1
                tmp = np.genfromtxt(data[start:stop]).T
                d_final = tmp[4]

                plt.figure(figsize=(10,5))
                plt.grid()
                plt.scatter(e_exp, d_init, label='fit init', c='blue')
                plt.scatter(e_exp, d_final, label='fit final', c='red')
                plt.legend(loc='upper left')
                plt.axhline(y=0, lw=1, color='black')
                plt.xlabel('E, cm${}^{-1}$')
                plt.ylabel(r'$\Delta$E, cm${}^{-1}$')
                plt.show()

            else:
                self.print_message(f'No plot options for mode \'{mode}\'\n')

        except BaseException as ex: # pylint: disable = W0718
            self.print_message(f'Failed to extract/visualize data from \'{fname}\'. Prob, it\'s modified manually.')

        return
