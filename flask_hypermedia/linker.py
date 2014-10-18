"""
Flask Hypermedia Link Map.

This module exports the ``LinkMap`` Flask application wrapper
that manages hypermedia actions for you.  See the docstring
for :class:`.LinkMap` for detailed description or the documentation
for this package for in-depth usage information.

"""
from __future__ import absolute_import

from . import exceptions


class LinkMap(object):

    """Maps hypermedia actions to registered rules.

    This class is the core of the Flask Hypermedia extension.  It
    incorporates itself into the routing mechanism within the flask
    application and keeps track of how you want to advertise routes
    for you.  There are a few ways to advertise actions using this
    extension:

    - include the ``advertise_as`` keyword when using the
      :meth:`flask.Flask.route` decorator
    - include the ``advertise_as`` keyword when calling
      :meth:`flask.Flask.add_url_rule`
    - explicitly call the :meth:`.advertise` method

    When this class wraps the :class:`flask.Flask` instance, it
    monkey-patches :meth:`~flask.Flask.add_url_rule` with
    :meth:`.add_url_rule`.  This makes it possible to add keyword
    parameters to  both :meth:`flask.Flask.add_url_rule` and
    :meth:`flask.Flask.route`.  The additional keyword parameters
    are used to advertise the rule without adding new API calls.

    This method does not work well when using method based views.
    In that case, you need to explicitly call :meth:`.advertise`
    to advertise a specific method of the view class.

    """

    def __init__(self, app):
        super(LinkMap, self).__init__()

    def add_url_rule(self, rule, endpoint=None, view_func=None, *args, **opts):
        """Monkey-patched version of :meth:`flask.Flask.add_url_rule`.

        :keyword str advertise_as: specify the name to advertise
            the generated rule with.  If this parameter is omitted,
            then the rule will not be advertised.
        :keyword str advertise_method: optionally specify the HTTP
            method to advertise the generated rule with.  If this
            parameter is omitted and it is not obvious which method
            should be advertised, :exc:`.exceptions.CannotDetermineMethod`
            will be raised.

        This method is inserted into the wrapped application and extends
        the underlying method and adds the keyword parameters that this
        extension depends on.

        """

    def advertise(self, link_name, method, view_class, endpoint=None):
        """Explicitly advertise a view class.

        :param str link_name: the name of the action to advertise
            the rule as.
        :param str method: the HTTP method that is being advertised.
        :param type view_class: the :class:`flask.views.MethodView`
            subclass to advertise.
        :param str endpoint: an optional endpoint name to advertise.

        """
