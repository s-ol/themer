#!/usr/bin/env python
# vim:fileencoding=utf-8:noet
from __future__ import unicode_literals
import os
import sys

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
try:
    README = open(os.path.join(here, 'README.md'), 'rb').read().decode('utf-8')
except IOError:
    README = ''

setup(
    name='Themer',
    version='0.2',
    description='Themer is a colorscheme generator and manager for your desktop.',
    long_description=README,
    author='Charles Leifer, Sol Bekic',
    author_email='s0lll0s@blinkenshell.org',
    url='https://github.com/S0lll0s/themer',
    scripts=[
        'scripts/themer',
        'scripts/wallfix'
    ],
    license='MIT',
    keywords='wm colorscheme color theme wallpaper',
    packages=find_packages(exclude=('tests', 'tests.*')),
    include_package_data=True,
    install_requires=['pyyaml','jinja2','pillow'],
    install_recommends=['kmeans']
)
