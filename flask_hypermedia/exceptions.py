"""
Flask Hypermedia Exceptions.

- ``LinkAdvertisementFailure``: catch-all exception for this extension.
  All other exceptions are sub-classes of this type.
- ``CannotDetermineMethod``: the extension needs help advertising a
  particular rule.
- ``MethodDoesNotExist``: you have tried to advertise a method that is
  not supported by a particular rule.
- ``AlreadyAdvertised``: you have advertised a rule twice.

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


class MethodDoesNotExist(LinkAdvertisementFailure):
    """You specified a method that is not supported.

    .. attribute:: failed_rule

       The rule that is being advertised.

    .. attribute:: specified_method

       The method that was specified and is not supported by
       :attr:`failed_rule`

    """


class AlreadyAdvertised(LinkAdvertisementFailure):
    """You tried to advertise the same link twice.

    .. attribute:: failed_rule

       The rule that could not be advertised.

    .. attribute:: existing_rule

       The rule that is already advertised.

    .. attribute:: link_name

       The name of the contentious link.

    """
