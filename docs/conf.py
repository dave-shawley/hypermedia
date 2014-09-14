#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sphinx_rtd_theme

from hypermedia import __version__, version_info


project = 'hypermedia'
copyright = '2014, Dave Shawley'
version = __version__
release = '.'.join(str(x) for x in version_info[:2])

needs_sphinx = '1.0'
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.intersphinx',
    'sphinx.ext.viewcode',
]
templates_path = []
source_suffix = '.rst'
source_encoding = 'utf-8-sig'
master_doc = 'index'
pygments_style = 'sphinx'
html_theme = 'sphinx_rtd_theme'
html_theme_path = [sphinx_rtd_theme.get_html_theme_path()]
html_static_path = []
exclude_patterns = []

intersphinx_mapping = {
    'python': ('http://docs.python.org/', None),
    'tornado': ('http://tornadoweb.org/en/branch4.0', None),
}
