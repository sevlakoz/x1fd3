from os.path import isfile, getsize
from warnings import warn

class Logger:
    '''
    class for writing results
    '''
    def __init__(
        self,
        mode: str = '',
        auto_name_adjust = True
    ) -> None:
        '''
        open file for results if name provided 
        optional automatic name adjust
        '''
        self.fname: str = mode
        if mode:
            if auto_name_adjust:
                n = 1
                while True:
                    self.fname = f'{mode}_{n}.log'
                    if isfile(self.fname) and getsize(self.fname) > 0:
                        n += 1
                    else:
                        break
            self.out = open(self.fname, 'w', encoding = 'utf-8')

    def print(
        self,
        *args,
        **kwargs
    ) -> None:
        '''
        print-like write to file or print to stdout if no file opened
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
            if len(args) > 0:
                self.out.write(str(args[0]))
                for mes in args[1:]:
                    self.out.write(kwargs['sep'])
                    self.out.write(str(mes))
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
            self.out = open(self.fname, 'w', encoding = 'utf-8')
        else:
            warn('Initialized with empty file name, skipping', RuntimeWarning)