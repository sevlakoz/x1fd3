from configparser import ConfigParser

class ExpData:
    '''
    class for storage vib. rot. levels
    '''
    def __init__(
        self,
        fname: str = ''
    ) -> None:
        '''
        init = read data if file provided 
        '''
        self.energy: dict[int, dict[int, float]] = {}

        if fname:
            self.read_file(fname)

    def read_file(
        self,
        fname: str
    ) -> None:
        '''
        read exp vib-rot levels from file
        format:
        [J]
        v E(v,J)
        ...
        '''
        input_parser = ConfigParser(delimiters=(' ', '\t'))
        input_parser.read(fname)

        # read levels
        n_levels = 0

        for j in input_parser.sections():
            tmp = {}
            for v, en in input_parser[j].items():
                tmp[int(v)] = float(en)
                n_levels += 1
            self.energy[int(j)] = tmp

        # check
        if n_levels == 0:
            raise RuntimeError(f'No energy levels found in {fname}')
