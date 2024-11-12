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
        print-like write to file
        print to stdout if no file opened on init
        '''
        if hasattr(self, 'out') and not self.out.closed:
            def_kwargs = {
                'sep': ' ',
                'end': '\n',
                'flush': True
            }
            for key, val in def_kwargs.items():
                if key not in kwargs:
                    kwargs[key] = val

            if 'file' in kwargs:
                warn('Writing to file opened on init, "file" option ignored', RuntimeWarning)

            if len(args) > 0:
                self.out.write(str(args[0]))
                for arg in args[1:]:
                    self.out.write(kwargs['sep'])
                    self.out.write(str(arg))
            self.out.write(kwargs['end'])

            if kwargs['flush']:
                self.out.flush()
        else:
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
