from themer import ThemeActivator
import os
try:
    import Image, ImageDraw
except ImportError:
    from PIL import Image, ImageDraw

# self.theme_dir = os.path.join(THEMER_ROOT, theme_name)
# self.colors = CachedColorParser(os.path.join(self.theme_dir,'colors.yaml')).read()

class WallfixActivator(ThemeActivator):
    def hex_to_rgb(self, h):
        h = h.lstrip('#')
        return tuple(map(lambda n: int(n, 16), [h[i:i+2] for i in range(0, 6, 2)]))

    def create_wallpaper(self, w=1920, h=1200, filename='wallpaper.png'):
        rectangles = (
            # x1, y1, x2, y2 -- in percents
            ('red', [0, 30.0, 3.125, 72.5]), # LEFT
            ('green', [50, 0, 76.5625, 12.5]), # TOP
            ('yellow', [96.875, 30.0, 100, 72.5]), # RIGHT
            ('magenta', [23.4375, 25.0, 50, 30.0]), # MID TOP LEFT
            ('white', [23.4375, 30.0, 50, 72.5]), # MID LEFT
            ('magenta', [50, 30.0, 76.5625, 72.5]), # MID RIGHT
            ('white', [50, 72.5, 76.5625, 87.5]), # MID BOTTOM RIGHT
        )
        def fix_coords(coords):
            m = [w, h, w, h]
            return [int(c * .01 * m[i]) for i, c in enumerate(coords)]
        background = self.hex_to_rgb(self.colors['black'])
        image = Image.new('RGB', (w, h), background)
        draw = ImageDraw.Draw(image)
        for color, coords in rectangles:
            x1, y1, x2, y2 = fix_coords(coords)
            draw.rectangle([(x1, y1), (x2, y2)], fill=self.hex_to_rgb(self.colors[color]))
        image.save(os.path.join(self.theme_dir, filename), 'PNG')
        return filename

    def activate(self):
        wallpaper = None
        for filename in os.listdir(self.theme_dir):
            if filename.startswith('wallpaper'):
                wallpaper = filename
                break
        if not wallpaper:
            self.logger.info('No wallpaper found in {}, generating new one.'.format(self.theme_dir))
            wallpaper = self.create_wallpaper()

        self.logger.info('Setting {} as wallpaper'.format(wallpaper))
        path = os.path.join(self.theme_dir, wallpaper)
        os.system('wallfix {}'.format(path)) # TODO: integrate wallfix here directly

exports = {
    "activators":   [ WallfixActivator ],
    "parsers":      []
}
