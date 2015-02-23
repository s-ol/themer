Themer
======

*Themer is a colorscheme generator and manager for your desktop.*

Installation
------------

First, check out the git repository:

    git clone https://github.com/S0lll0s/themer.git

Install with `python setup.py install`

    cd themer
    sudo python setup.py install

I am working on getting an AUR package for this. It might also end up in PyPI in the future.

Configuration
-------------

You can create multiple template dirs for `themer` in `~/.config/themer/templates`.
The default template is `i3`; see [config/default](config/default) for the default configuration.


Usage
-----

### Generating Themes

Generate a theme from a wallpaper:

    $ themer generate themename /absolute/path/to/wallpaper.png

...or install a colorscheme from `sweyla.com`:
 
    $ themer generate themename 693812

(this will install [http://sweyla.com/themes/seed/693812/](http://sweyla.com/themes/seed/693812/))

finally, you can also use an Xresources-style file:

    $ themer generate themename /home/me/.Xresources

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
