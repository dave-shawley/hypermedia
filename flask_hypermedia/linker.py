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
        self.__link_map = {}
        self._real_add_url_rule = app.add_url_rule
        app.add_url_rule = self.add_url_rule

        self._app = app
        self.logger = app.logger.getChild('LinkMap')

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
        link_name = opts.pop('advertise_as', None)
        link_method = opts.pop('advertise_method', None)

        result = self._real_add_url_rule(rule, endpoint, view_func,
                                         *args, **opts)
        if link_name is None:
            return result

        # Find the rule that matches the endpoint + view_func
        # parameters.  The tricky part is that both are optional
        # AND they are meaningful together - IOW, all permutations
        # of {endpoint, view_func} are valid :/
        matched = None
        for rule_obj in self._app.url_map.iter_rules(endpoint=endpoint):
            registered = self._app.view_functions.get(rule_obj.endpoint, None)
            if endpoint is not None:
                if rule_obj.endpoint == endpoint:
                    if view_func is None or registered == view_func:
                        matched = rule_obj
            elif view_func is not None and registered == view_func:
                matched = rule_obj

        # Now we get to figure out which HTTP method to advertise.
        # If we weren't given one explicitly, we will advertise
        # a non-meta method if there is only one; otherwise, bail
        # since the result is indeterminate.
        if link_method is None:
            methods = set(matched.methods) - set(['HEAD', 'OPTIONS'])
            if len(methods) != 1:
                raise exceptions.CannotDetermineMethod(matched)
            link_method = methods.pop()

        self._link_rule(link_name, link_method, matched)

        return result

    def advertise(self, link_name, method, view_class, endpoint=None):
        """Explicitly advertise a view class.

        :param str link_name: the name of the action to advertise
            the rule as.
        :param str method: the HTTP method that is being advertised.
        :param type view_class: the :class:`flask.views.MethodView`
            subclass to advertise.
        :param str endpoint: an optional endpoint name to advertise.

        """

    def _link_rule(self, link_name, method, rule):
        if link_name in self.__link_map:
            raise exceptions.AlreadyAdvertised(
                rule, self.__link_map[link_name], link_name)

        if method not in rule.methods:
            self.logger.error('%s is not supported by %r', method, rule)
            raise exceptions.MethodDoesNotExist(rule, method)

        self.logger.debug('advertising %s %r as %s', method, rule, link_name)
        self.__link_map[link_name] = {'method': method, 'rule': rule}

    def __getitem__(self, action_name):
        return self.__link_map[action_name]
