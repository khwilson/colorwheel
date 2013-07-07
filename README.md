Colorwheel
==========
A simple python class which will yield iterators of rgb strings of a specified
number of distinct colors in a specified range.

Written and maintained by [Kevin Wilson](http://www.github.com/khwilson). Last
updated July 2013.

Usage
-----
```python
import colorwheel

# How many colors do you want?
num_colors = 10
palette = colorwheel.make_palette(num_colors)

# Or do you just want to rotate through them?
wheel = colorwheel.make_wheel(num_colors)
```

Inspiration
-----------
I was using [IWantHue](http://tools.medialab.sciences-po.fr/iwanthue/) for a
while on the suggestion of [Aurelia Moser](aureliamoser.com), but I really
wanted a python library which did the same thing.

Of course, much of IWantHue was actually based on the excellent work of
[Gregor Aisch](http://driven-by-data.net) on his
[Chroma.js](github.com/gka/chroma.js). The entire utils.py file was ganked
from either wikipedia or from this lovely library and was tested against
Chroma using Chrome's console.

License
-------
(C) 2013 Kevin Wilson. MIT Licensed. See LICENSE for full license statement.
