import unittest

try:
    from unittest import mock
except ImportError:
    # noinspection PyPackageRequirements
    import mock

__all__ = ('mock', 'unittest')
