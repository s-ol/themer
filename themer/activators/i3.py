from themer import ThemeActivator
import os

class I3Activator(ThemeActivator):
    def activate(self):
        os.system('i3-msg -q restart')
