import os
import re
import yaml

class ThemeActivator(object):
    def __init__(self, theme_name, theme_dir, logger):
        self.theme_name = theme_name
        self.theme_dir  = theme_dir
        self.logger     = logger
        self.colors     = CachedColorParser(os.path.join(self.theme_dir, 'colors.yaml'), logger).read()

    def activate(self):
        pass

class ColorParser(object):
    # Colors look something like "*color0:  #FF0d3c\n"
    color_re = re.compile('.*?(color[^:]+|background|foreground):\s*(#[\da-z]{6})')

    def __init__(self, color_file, logger):
        self.color_file = color_file
        self.logger = logger
        self.colors = {}

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

        with open(self.color_file) as fh:
            for line in fh.readlines():
                if line.startswith('!'):
                    continue
                match_obj = self.color_re.search(line.lower())
                if match_obj:
                    var, color = match_obj.groups()
                    self.colors[color_mapping[var]] = color

        if len(self.colors) < 16:
            logger.warning(
                'Error, only {} colors were read when loading color file "{}"'
                .format(len(self.colors), self.color_file))
        return self.colors

class CachedColorParser(ColorParser):
    def read(self):
        with open(self.color_file) as fh:
            self.colors = yaml.load(fh)
        return self.colors
