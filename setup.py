#!/usr/bin/env python
# vim:fileencoding=utf-8:noet
from __future__ import unicode_literals
import os
import sys

from setuptools import setup, find_packages
from setuptools.command.install import install

here = os.path.abspath(os.path.dirname(__file__))
try:
    README = open(os.path.join(here, 'README.md'), 'rb').read().decode('utf-8')
except IOError:
    README = ''

class new_install(install):
    def run(self):
        install.run(self) # invoke original install
        self.mkpath('/usr/share/themer')
        self.copy_tree('data/default', '/usr/share/themer/default')
        self.mkpath('/usr/share/fish/completions')
        self.copy_file('data/fish/themer.fish', '/usr/share/fish/completions/')

setup(
    name='Themer',
    version='1.1',
    description='Themer is a colorscheme generator and manager for your desktop.',
    long_description=README,
    author='Charles Leifer, Sol Bekic',
    author_email='s0lll0s@blinkenshell.org',
    url='https://github.com/S0lll0s/themer',
    scripts=['scripts/themer'],
    license='MIT',
    keywords='wm colorscheme color theme wallpaper',
    packages=find_packages(exclude=('tests', 'tests.*')),
    include_package_data=True,
    install_requires=['pyyaml','jinja2','pillow'],
    cmdclass=dict(install=new_install)
)
