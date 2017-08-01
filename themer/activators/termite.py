from themer import ThemeActivator
import os

class TermiteActivator(ThemeActivator):
    """Tell termite to reload configuration file"""
    def activate(self):
        os.system('killall -s USR1 termite')
