from os.path import isfile, getsize

class Logger:
    '''
    init = open file for results, automatic name selection for CLI versions
    '''
    def __init__(
        self,
        mode: str = '',
        is_gui = False
    ) -> None:
        '''
        2
        '''
        if mode:
            if is_gui:
                self.fname = mode
            else:
                n = 1
                while True:
                    self.fname = f'{mode}_{n}.log'
                    if isfile(self.fname) and getsize(self.fname) > 0:
                        n += 1
                    else:
                        break
            self.out = open(self.fname, 'w', encoding = 'utf-8')
        else:
            self.fname = ''

    def print(
        self,
        *args,
        **kwargs
    ) -> None:
        '''
        print-like write to file
        '''
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

    def close(
        self
    ) -> None:
        '''
        close file 
        '''
        self.out.close()
