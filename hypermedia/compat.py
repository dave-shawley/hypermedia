"""
Python 2-3 compatibility layer.

Similar in vein to libraries like ``six`` but much lighter in
weight, this module exports a common interface that hides the
differences between the Python 2 and Python 3 standard libraries.

"""
try:
    from urllib.parse import (
        parse_qs, quote, urlencode, urljoin, urlsplit, urlunsplit)
except ImportError:  # pragma: no cover
    # noinspection PyUnresolvedReferences
    from urllib import quote, urlencode
    # noinspection PyUnresolvedReferences
    from urlparse import parse_qs, urljoin, urlsplit, urlunsplit


__all__ = (
    'parse_qs',
    'quote',
    'urlencode',
    'urljoin',
    'urlsplit',
    'urlunsplit',
)
