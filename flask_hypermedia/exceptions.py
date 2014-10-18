"""
Flask Hypermedia Exceptions.

- ``LinkAdvertisementFailure``: catch-all exception for this extension.
  All other exceptions are sub-classes of this type.
- ``CannotDetermineMethod``: the extension needs help advertising a
  particular rule.

"""


class LinkAdvertisementFailure(Exception):
    """Flask Hypermedia failed to advertise a link.

    This is a _root_ exception type that acts as a catch all
    exception for the Flask Hypermedia extension.

    """
    pass


class CannotDetermineMethod(LinkAdvertisementFailure):
    """Flask Hypermedia needs some help advertising a link.

    .. attribute:: failed_rule

       The rule in question.

    This exception is raised when the extension cannot determine
    which HTTP method to advertise a link with.  In many cases it
    is obvious which method to advertise, when it isn't you need
    to specify it explicitly using the ``advertise_method`` keyword
    parameter.

    """
