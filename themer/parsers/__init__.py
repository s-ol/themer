from themer import ColorParser, check_file_regex

import os
import re
import math
import yaml
import requests #urllib.request
import random
from tempfile import mkstemp

class CachedColorParser(ColorParser):
    check = check_file_regex('^colors\.yaml$')

    def read(self):
        with open(self.data) as fh:
            self.colors = yaml.load(fh)
        return self.colors

class SweylaColorParser(ColorParser):
    check = '^(sweyla)?[0-9]+$'

    def mapping(self):
        return {
            'bg': ['background', 'black', 'alt_black'],
            'fg': ['foreground', 'white'],
            'nf': 'red',  # name of function / method
            'nd': 'alt_red',  # decorator
            'nc': 'green',  # name of class
            'nt': 'alt_green', # ???
            'nb': 'yellow',  # e.g., "object" or "open"
            'c': 'alt_yellow',  # comments
            's': 'blue',  # string
            'mi': 'alt_blue',  # e.g., a number
            'k': 'magenta',  # e.g., "class"
            'o': 'alt_magenta', # operator, e.g "="
            'bp': 'cyan',  # e.g., "self" keyword
            'si': 'alt_cyan', # e.g. "%d"
            'se': 'alt_white',
            'support_function': 'underline'}

    def read(self):
        mapping = self.mapping()
        resp = requests.get(
            'http://sweyla.com/themes/textfile/sweyla{}.txt'.format(
                re.search("([0-9]+)",self.data).groups()[0]))
        contents = resp.text
        for line in contents.splitlines():
            key, value = line.split(':\t')
            if key in mapping:
                colors = mapping[key]
                if not isinstance(colors, list):
                    colors = [colors]
                for color in colors:
                    self.colors[color] = value
        return self.colors

# TODO: "lazy" loading somehow?
import colorsys
import itertools
try:
    import Image, ImageDraw
except ImportError:
    from PIL import Image, ImageDraw

try:
    import kmeans
except ImportError:
    global kmeans

    class PyKmeans:
        def ec_dist(self, a, b):
            return math.sqrt(
                sum((a[0][i] - b[0][i]) ** 2 for i in range(3)))

        def c_center(self, points):
            vals = [0.0 for i in range(3)]
            plen = 0
            for p in points:
                plen += p[1]
                for i in range(3):
                    vals[i] += p[0][i] * p[1]
            return ([(v/plen) for v in vals], 1)

        def kmeans(self, points, k, min_diff=1):
            print("""Falling back to python kmeans implementation.
            Consider installing 'kmeans' from PyPI for much faster image sampling""")
            clusters = [([p], p) for p in random.sample(points, k)]
            while True:
                plists = [[] for i in range(k)]
                for p in points:
                    smallest_distance = float('Inf')
                    for i in range(k):
                        distance = self.ec_dist(p, clusters[i][1])
                        if distance < smallest_distance:
                            smallest_distance = distance
                            idx = i
                    plists[idx].append(p)
                diff = 0
                for i in range(k):
                    old = clusters[i]
                    center = self.c_center(plists[i])
                    new = (plists[i], center)
                    clusters[i] = new
                    diff = max(diff, self.ec_dist(old[1], new[1]))
                if diff <= min_diff:
                    break
            return [map(int, c[1][0]) for c in clusters]

    kmeans = PyKmeans()

class KmeansColorParser(ColorParser):
    check = check_file_regex('\.(jpg|png|jpeg)$')

    def __init__(self, wallpaper, config, logger, k=16, bg='#0e0e0e', fg='#ffffff'):
        self.wallpaper = wallpaper
        self.config = config
        self.logger = logger
        self.bg = bg
        self.fg = fg
        self.k = k

    def _get_points_from_image(self, img):
        points = []
        w, h = img.size
        for count, color in img.getcolors(w * h):
            points.append((color, count))
        return points

    def rgb_to_hex(self, rgb):
        return '#{}'.format(''.join(('%02x' % int(p) for p in rgb)))

    def hex_to_rgb(self, h):
        h = h.lstrip('#')
        return tuple(map(lambda n: int(n, 16), [h[i:i+2] for i in range(0, 6, 2)]))

    def get_dominant_colors(self):
        img = Image.open(self.wallpaper)
        img.thumbnail((300, 300))  # Resize to speed up python loop.
        width, height = img.size
        points = self._get_points_from_image(img)
        rgbs = kmeans.kmeans(points, self.k)
        #rgbs = [map(int, c.center.coords) for c in clusters]
        return [self.rgb_to_hex(rgb) for rgb in rgbs]

    def normalize(self, hexv, minv=128, maxv=256):
        r, g, b = self.hex_to_rgb(hexv)
        h, s, v = colorsys.rgb_to_hsv(r / 256.0, g / 256.0, b / 256.0)
        minv = minv / 256.0
        maxv = maxv / 256.0
        if v < minv:
            v = minv
        if v > maxv:
            v = maxv
        rgb = colorsys.hsv_to_rgb(h, s, v)
        return self.rgb_to_hex(map(lambda i: i * 256, rgb))

    def read(self):
        colors = self.get_dominant_colors()
        color_dict = {
            'background': self.bg,
            'foreground': self.fg}
        for i, color in enumerate(itertools.cycle(colors)):
            if i == 0:
                color = self.normalize(color, minv=0, maxv=32)
            elif i == 8:
                color = self.normalize(color, minv=128, maxv=192)
            elif i < 8:
                color = self.normalize(color, minv=160, maxv=224)
            else:
                color = self.normalize(color, minv=200, maxv=256)
            color_dict['color%d' % i] = color
            if i == 15:
                break
        mapping = self.mapping()
        translated = {}
        for k, v in color_dict.items():
            translated[mapping[k]] = v
        return translated

class WallhavenColorParser(KmeansColorParser):
    check = 'wallhaven.cc/wallpaper/[0-9]+$'

    def __init__(self, wallpaper, config, logger, k=16, bg='#0e0e0e', fg='#ffffff'):
        wallid = re.search("([0-9]+)", wallpaper).groups()[0]
        suffix = '.jpg'
        res = requests.get('http://wallpapers.wallhaven.cc/wallpapers/full/wallhaven-{}.jpg'.format(wallid), stream=True)

        if not res.ok:
            res = requests.get('http://wallpapers.wallhaven.cc/wallpapers/full/wallhaven-{}.png'.format(wallid), stream=True)
            suffix = '.png'

        (dest, path) = mkstemp(suffix=suffix)

        for block in res.iter_content(1024):
            os.write(dest, block)
        os.close(dest)

        super(WallhavenColorParser, self).__init__(path, config, logger, k, bg, fg)

    def read(self, *args):
        res = super(WallhavenColorParser, self).read(*args)
        return res
