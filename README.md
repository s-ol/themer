Themer
======

*Themer is a colorscheme generator and manager for your desktop.*

Installation
------------

### AUR (Arch)

Install [python-themer-git](https://aur.archlinux.org/packages/python-themer-git/) with the AUR manager of your choice:

    $ yaourt -S python-themer-git

### Manual Installation

First, check out the git repository:

    $ git clone https://github.com/S0lll0s/themer.git

Install with `python setup.py install`

    $ cd themer
    $ sudo python setup.py install

Ihis package might also end up in PyPI in the future.

Configuration
-------------

You can create multiple template dirs for `themer` in `~/.config/themer/templates`.
The default template is `i3`; see [config/default](config/default) for the default configuration.


Usage
-----

### Generating Themes

Generate a theme from a wallpaper:

    $ themer generate themename wallpaper.png

...or install a colorscheme from `sweyla.com`:
 
    $ themer generate themename 693812

(this will install [http://sweyla.com/themes/seed/693812/](http://sweyla.com/themes/seed/693812/))

you can also use an Xresources-style file:

    $ themer generate themename /home/me/.Xresources

[Plugins](#plugins) enable you to generate themes from other sources as well, see below.

### Viewing Installed Themes

You can list all generated themes with `themer list`:

    $ themer list
    themeone
    themetwo

### Activating Themes

You can activate an existing theme with `themer activate`:

    $ themer activate sometheme

This will symlink all defined templates to `~/.config/themer/current`. You should, in turn, symlink all the global configuration files to there. For example for i3:

    $ ln -s ~/.config/themer/current/i3.conf ~/.i3/config

To view the currently activated theme's colors use `themer current`.

If you have modified the templates, activating the theme again will not apply those changes. Instead
use `themer render` to update your configuration:

    $ themer render sometheme

### Deleting Themes

Deleting generated themes is possible using `themer delete`:

    $ themer delete sometheme

Screenshots
-----------

![](http://media.charlesleifer.com/blog/photos/candybean.png)
![](http://media.charlesleifer.com/blog/photos/bloom.png)
![](http://media.charlesleifer.com/blog/photos/waves.png)
![](http://media.charlesleifer.com/blog/photos/waves2.png)

Plugins
-------

Plugins can be installed into `~/.config/themer/plugins`. A plugin is a python module that sets a variable called `exports`.

`exports` is a dictionary that needs to have the two keys `activators` and `parsers`, both of which should resolve to a list. Activators should inherit from `themer.ThemeActivator`, Parsers should inherit from `themer.ColorParser`.

### `ThemeActivator`s
The list of activators is simply a list of those classes and will be merged into the "global" list of activators.

Each Activator should implement the method `activate`.
The constructor is passed the values for `theme_name`, `theme_dir` and `logger`.
All of these and `colors` can be accessed via the instance's properties.

#### Example:

    from themer import ThemeActivator
    import os
    
    class I3Activator(ThemeActivator):
        def activate(self):
            os.system('i3-msg -q restart')
    
    exports = {
        "activators":   [ I3Activator ],
        "parsers":      []
    }

### `ColorParser`s
The "parsers" list should contain tuples of a `matcher` and the class/type; the matcher can be either a string, a compiled regex (`re`) or a function. If it is a string it will be used as a regex as well. Whenever the `matcher` matches (the function returns `True`) the `ColorParser` will be used.

Each ColorParser should implement the method `read`, which should return the color dictionary generated from the input string in `self.data` (or obtained via the constructor's first argument).
A ColorParser can additionally return a path to a wallpaper to be used by setting `self.wallpaper` to anything other than `None`.

The constructor is passed the values for `data`, `config` and `logger`.
All of these can be accessed via the instance's properties.
The default constructor also sets `self.colors` to a new dictionary and `self.wallpaper` to `None`.

#### Example:

    from themer import ColorParser

    class NewColorParser(ColorParser):
        def read(self):
            with open(self.data) as fh: # load colors from a yaml file
                self.colors = yaml.load(fh)
            return self.colors

    exports = {
        "activators": [],
        "parsers":    [ ("\.yaml$", NewColorParser) ]
    }

Credits
-------

Original script by [Charles Leifer](https://github.com/coleifer)  
Maintained and developed further by [Sol Bekic](https://github.com/S0lll0s)
