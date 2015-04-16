from themer import ThemeActivator
import os
try:
    import Image, ImageDraw
except ImportError:
    from PIL import Image, ImageDraw

HOME = os.environ['HOME']

try:
    import re
    screen_info = os.popen('xrandr').readlines()
    resolution_re = re.compile('\s+(\d+)x(\d+)\s+\d+\.\d+\*')
    for line in screen_info:
        match_obj = resolution_re.search(line)
        if match_obj:
            WIDTH, HEIGHT = map(int, match_obj.groups())
            break
except:
    WIDTH = 1440
    HEIGHT = 900
RATIO = float(WIDTH) / HEIGHT


class WallfixActivator(ThemeActivator):
    def hex_to_rgb(self, h):
        h = h.lstrip('#')
        return tuple(map(lambda n: int(n, 16), [h[i:i+2] for i in range(0, 6, 2)]))

    def new_wallpaper(self, w=1920, h=1200, filename='wallpaper.png'):
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
        return image

    def crop_wallpaper(self, image):
        width, height = image.size
        ratio = float(width) / height

        if ratio > RATIO:
            # resize to match height, then crop horizontally from center
            new_width = int(HEIGHT * ratio)
            image.thumbnail((new_width, HEIGHT), Image.ANTIALIAS)
            offset = int((new_width - WIDTH) / 2)
            cropped = image.crop((offset, 0, offset + WIDTH, HEIGHT))
        elif ratio < RATIO:
            # resize to match width, then crop vertically from center
            new_height = int(WIDTH / ratio)
            image.thumbnail((WIDTH, new_height), Image.ANTIALIAS)
            offset = int((new_height - HEIGHT) / 2)
            cropped = image.crop((0, offset, WIDTH, offset + HEIGHT))
        else:
            image.thumbnail((WIDTH, HEIGHT), Image.ANTIALIAS)
            cropped = image

        dest_jpg = os.path.join(HOME, '.wallpaper.jpg')
        dest_png = os.path.join(HOME, '.wallpaper.png')

        cropped.save(dest_jpg, 'JPEG', quality=100)
        cropped.save(dest_png, 'PNG')

    def activate(self):
        wallpaper = None
        for filename in os.listdir(self.theme_dir):
            if filename.startswith('wallpaper'):
                wallpaper = Image.open(os.path.join(self.theme_dir, filename))
                break
        if not wallpaper:
            self.logger.info('No wallpaper found in {}, generating new one.'.format(self.theme_dir))
            wallpaper = self.new_wallpaper()

        self.logger.info('Setting new wallpaper')
        self.crop_wallpaper(wallpaper)
