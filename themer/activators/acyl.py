from themer import ThemeActivator
import re
import os

class ACYLActivator(ThemeActivator):
    def icon_path(self):
        return os.path.join(os.environ['HOME'], '.icons/acyl')

    def primary_icon(self):
        return os.path.join(self.icon_path(), 'scalable/places/desktop.svg')

    def secondary_icon(self):
        return os.path.join(self.icon_path(), 'scalable/actions/add.svg')

    def extract_color_svg(self, filename):
        regex = re.compile('stop-color:(#[\da-zA-Z]{6})')
        with open(filename, 'r') as fh:
            for line in fh.readlines():
                match_obj = regex.search(line)
                if match_obj:
                    return match_obj.groups()[0]
        raise ValueError('Unable to determine icon color.')

    def activate(self):
        old_primary = self.extract_color_svg(self.primary_icon())
        old_secondary = self.extract_color_svg(self.secondary_icon())
        logger.debug('Old icon colors: {}, {}'.format(old_primary, old_secondary))

        # Walk the icons, updating the colors in each svg file.
        file_count = 0
        for root, dirs, filenames in os.walk(self.icon_path()):
            for filename in filenames:
                if not filename.endswith('.svg'):
                    continue
                path = os.path.join(root, filename)
                with open(path, 'r+') as fh:
                    contents = fh.read()
                    contents = contents.replace(old_primary, self.colors["primary"])
                    contents = contents.replace(old_secondary, self.colors["secondary"])
                    fh.seek(0)
                    fh.write(contents)
                    file_count += 1
        logger.info('Checked {} icon files'.format(file_count))
