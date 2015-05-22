import os.path
import re

def check_file_regex(regex):
    """Builds a function that checks wheter a filename matches 'regex' and corresponds to an existing file.

    For use as a ColorParser's 'check' attribute."""
    return staticmethod(lambda src: re.search(regex, src, re.IGNORECASE) and os.path.isfile(src))

class ThemeActivator(object):
    def __init__(self, theme_name, theme_dir, logger):
        from themer.parsers import CachedColorParser

        self.theme_name = theme_name
        self.theme_dir  = theme_dir
        self.logger     = logger
        self.colors     = CachedColorParser(os.path.join(self.theme_dir, 'colors.yaml'), None, logger).read()

    def activate(self):
        pass

class ColorParser(object):
    check = check_file_regex('(.*)')

    # Colors look something like "*color0:  #FF0d3c\n"
    color_re = re.compile('.*?(color[^:]+|background|foreground):\s*(#[\da-z]{6})')

    def __init__(self, data, config, logger):
        self.data = data
        self.config = config
        self.logger = logger
        self.colors = {}
        self.wallpaper = None

    def mapping(self):
        return {
            'background': 'background',
            'foreground': 'foreground',
            'color0': 'black',
            'color8': 'alt_black',
            'color1': 'red',
            'color9': 'alt_red',
            'color2': 'green',
            'color10': 'alt_green',
            'color3': 'yellow',
            'color11': 'alt_yellow',
            'color4': 'blue',
            'color12': 'alt_blue',
            'color5': 'magenta',
            'color13': 'alt_magenta',
            'color6': 'cyan',
            'color14': 'alt_cyan',
            'color7': 'white',
            'color15': 'alt_white',
            'colorul': 'underline'}

    def read(self):
        color_mapping = self.mapping()

        with open(self.data) as fh:
            for line in fh.readlines():
                if line.startswith('!'):
                    continue
                match_obj = self.color_re.search(line.lower())
                if match_obj:
                    var, color = match_obj.groups()
                    self.colors[color_mapping[var]] = color

        if len(self.colors) < 16:
            self.logger.warning(
                'Error, only {} colors were read when loading color file'
                .format(len(self.colors)))
        return self.colors
