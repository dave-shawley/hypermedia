"""
Hypermedia helper library.

This library is an attempt to simplify the generation and use
of hypermedia controls in HTTP representations.  This module,
however, serves a much simpler and more direct purpose.  It
exports the version information for the library AND DOES
NOTHING ELSE!  Most importantly, IT DOES NOT IMPORT OR DEFINE
ANYTHING!!

"""
version_info = (0, 0, 0)
__version__ = '.'.join(str(x) for x in version_info)
