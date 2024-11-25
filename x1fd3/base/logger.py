from os.path import isfile, getsize
from warnings import warn
from typing import TextIO, Any

class Logger:
    '''
    class for writing results
    '''
    def __init__(
        self,
        fname:str='',
        auto_name_adjust:bool=True
    ) -> None:
        '''
        open file for results if name provided,
        automatic adjust file name by default
        '''
        self.fname:str = fname
        if fname:
            if auto_name_adjust:
                n = 1
                while True:
                    self.fname = f'{fname}_{n}.log'
                    if isfile(self.fname) and getsize(self.fname) > 0:
                        n += 1
                    else:
                        break
            self.out:TextIO = open(self.fname, 'w', encoding='utf-8')

    def print(
        self,
        *args:Any,
        **kwargs:Any
    ) -> None:
        '''
        print to file opened on init
        print to stdout/file set by "file=" otherwise
        forced "flush=True"
        '''
        if 'file' not in kwargs and hasattr(self, 'out'):
            if self.out.closed:
                warn('File opened on init is closed, "file" kwarg not provided, print to stdout', RuntimeWarning)
            else:
                kwargs['file'] = self.out

        kwargs['flush'] = True

        print(*args, **kwargs)

    def close(
        self
    ) -> None:
        '''
        close file 
        '''
        if hasattr(self, 'out'):
            self.out.close()
        else:
            warn('Initialized with empty file name, skipping', RuntimeWarning)

    def reopen(
        self
    ) -> None:
        '''
        reopen
        '''
        if hasattr(self, 'out'):
            self.out = open(self.fname, 'w', encoding='utf-8')
        else:
            warn('Initialized with empty file name, skipping', RuntimeWarning)
