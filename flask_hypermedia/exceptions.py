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
    def __init__(self, rule):
        super(CannotDetermineMethod, self).__init__(rule)
        self.failed_rule = rule

    def __str__(self):
        return (
            'cannot determine method to advertise for {0!s}. You need '
            'to specify the advertise_method keyword in this case.'
        ).format(self.failed_rule)


class MethodDoesNotExist(LinkAdvertisementFailure):
    """You specified a method that is not supported.

    .. attribute:: failed_rule

       The rule that is being advertised.

    .. attribute:: specified_method

       The method that was specified and is not supported by
       :attr:`failed_rule`

    """
    def __init__(self, rule, method):
        super(MethodDoesNotExist, self).__init__(rule, method)
        self.failed_rule = rule
        self.specified_method = method

    def __str__(self):
        return '{0!s} does not support {1}'.format(
            self.failed_rule, self.specified_method)


class AlreadyAdvertised(LinkAdvertisementFailure):
    """You tried to advertise the same link twice.

    .. attribute:: failed_rule

       The rule that could not be advertised.

    .. attribute:: existing_rule

       The rule that is already advertised.

    .. attribute:: link_name

       The name of the contentious link.

    """
    def __init__(self, rule, existing_rule, link_name):
        super(AlreadyAdvertised, self).__init__(existing_rule, link_name)
        self.failed_rule = rule
        self.existing_rule = existing_rule
        self.link_name = link_name

    def __str__(self):
        return '{0} is already advertised as {1!s}'.format(
            self.link_name, self.existing_rule)
