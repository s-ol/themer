from themer.parsers import KmeansColorParser

from tempfile import mkstemp
import re
import requests
import os

class UnsplashColorParser(KmeansColorParser):
    check = 'unsplash.com/.*photo=[_\w\d]+$'

    def __init__(self, wallpaper, config, logger, k=16, bg='#0e0e0e', fg='#ffffff'):
        wallid = re.search("=([_\w\d]+)$", wallpaper).groups()[0]
        url = "http://unsplash.com/photos/{}/download".format(wallid)
        suffix = '.jpg'
        res = requests.get(url, stream=True)
        (dest, path) = mkstemp(suffix=suffix)
        for block in res.iter_content(1024):
            os.write(dest, block)
        os.close(dest)
        super(UnsplashColorParser, self).__init__(path, config, logger, k, bg, fg)

    def read(self, *args):
        return super(UnsplashColorParser, self).read(*args)
