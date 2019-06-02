=====
NCL Colormaps
=====

This library aims to define all NCL color tables as ListedColormap objects for
use in plotting with matplotlib.pyplot (and maybe others, but this is the main
focus). Matplotlib colormaps are also defined within for convenience.

Functions included will assist with loading and defining NCL color tables and
matplotlib colormaps as ListedColormap objects, and will also allow the user to
create new colormaps from any combination of those avaialable in the library.

NOTE: it is easy to misrepresent your data with color! Please choose your colormap
wisely, and even more importantly, pay attention to how you build custom colormaps.
The authors strongly suggest reading about how colormaps are perceived. For example:

http://web.archive.org/web/20180201210047/www.research.ibm.com/people/l/lloydt/color/color.HTM

The authors are not liable for any misinterpretation of your data through use of
this library or otherwise.
