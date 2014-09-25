"""
Mix-ins for Tornado.

This module contains mixin classes that assist with writing hypermedia
based Tornado applications.  Each class is designed to be mixed-in
over one of the classes defined in :mod:`tornado.web`.

- :class:`.Linker`: :class:`~tornado.web.RequestHandler` mixin that
  imbues the handler with a map of hyperlinked actions.

"""
from tornado import web

from .. import compat


class Linker(object):

    r"""
    Mix this in over ``RequestHandler`` to enable hyperlink generation.

    This mix-in adds a few helper methods for generating a :class:`dict`
    of named action and associated hyperlink information.  It should be
    mixed in over :class:`tornado.web.RequestHandler`.  It depends on
    the following attributes:

    .. attribute:: application

       Should be an instance of :class:`tornado.web.Application` but
       only the ``handlers`` attribute is used.  It is a sequence
       that contains (host pattern, url spec) tuples.  *Host pattern* is
       a compiled regular expression (:func:`re.compile`) that identifies
       the host pattern that a set of URLs corresponds to.  *Url spec* is
       a object that quacks like :class:`tornado.web.URLSpec`.
       sub-groups for each path parameter and *url spec*

    .. attribute:: request

       Usually an instance of :class:`tornado.httputil.HTTPServerRequest`.
       The :meth:`~tornado.httputil.HTTPServerRequest.full_url` method is
       used to retrieve the base URL to relativize against.

    The generated mapping is a :class:`dict` where the hypermedia action
    name is the key and a :class:`dict` containing the absolute URL and
    the appropriate HTTP method is the value.

    .. code-block:: python

        class PersonHandler(Linker, web.RequestHandler):
            def get(self, uid):
                self.add_link(
                    'relationships', RelationshipHandler, 'GET', uid=uid)

        class RelationshipHandler(Linker, web.RequestHandler):
            def get(self, uid):
                self.add_link('self', PersonHandler, 'GET', uid=uid)
                self.add_link('sisters', SiblingHandler, 'GET',
                              relation='sister', uid=uid)
                self.add_link('brothers', SiblingHandler, 'GET',
                              relation='brother', uid=uid)
                self.add_link('create', RelationshipHandler, 'POST', uid=uid)

            def post(self, uid):
                pass

        class SiblingHandler(Linker, web.RequestHandler):
            def get(self, uid, relation):
                pass

        app = web.Application([
            (r'/(?P<uid>\d+)', PersonHandler),
            (r'/(?P<uid>\d+)/relationships', RelationshipHandler),
            (r'/(?P<uid>\d+)/siblings/(?P<relation>\s+)', SiblingHandler),
        ])

    The link map for ``PersonHandler`` when it is created for
    ``http://example.com:8080/42`` would look like:

    .. code-block:: json

        {
            "relationships": {
                "method": "GET",
                "url": "http://example.com:8080/42/relationships"
            }
        }

    Similarly, the link map for ``RelationshipHandler`` would be:

    .. code-block:: json

        {
            "brothers": {
                "method": "GET",
                "url": "http://example.com/42/siblings/brother"
            },
            "create": {
                "method": "POST",
                "url": "http://example.com/42/siblings"
            },
            "self": {
                "method": "GET",
                "url": "http://example.com/42"
            },
            "sisters": {
                "method": "GET",
                "url": "http://example.com/42/siblings/sister"
            }
        }

    """

    def __init__(self, *args, **kwargs):
        # noinspection PyArgumentList
        super(Linker, self).__init__(*args, **kwargs)
        self.__link_map = {}
        sentinel = object()
        if getattr(self, 'request', sentinel) is sentinel:
            self.request = None
        if getattr(self, 'application', sentinel) is sentinel:
            self.application = None

    def add_link(self, name, handler, method, query=None, **kwargs):
        """
        Add a link to a specific handler to the map.

        :param str name: the name of the link to add
        :param tornado.web.RequestHandler handler: target this handler
            with the generated URL
        :param str method: the HTTP method for the link
        :param dict query: parameters for the URL query or ``None``
        :param kwargs: parameters to substitute into the handler's path

        :raises tornado.web.HTTPError: if ``handler`` is not registered
            for the currently active host or a path parameter is omitted
            from ``kwargs``

        """
        matched_spec = self._find_handler_for_class(handler)
        next_url = compat.urljoin(self.request.full_url(),
                                  self._build_path_args(matched_spec, kwargs))
        if query is not None:
            next_url = self._rewrite_query(next_url, query)

        self.__link_map[name] = {'method': method, 'url': next_url}

    def add_external_link(self, name, method, url, query=None):
        """
        Add a raw URL link.

        :param str name: the name of the link to add
        :param str method: the HTTP method for the link
        :param str url: the URL to advertise
        :param dict query: parameters for the URL query or ``None``

        """
        if query is not None:
            url = self._rewrite_query(url, query)
        self.__link_map[name] = {'method': method, 'url': url}

    def get_link_map(self):
        """Return a :class:`dict` containing the generated link map."""
        return self.__link_map

    def _find_handler_for_class(self, cls):
        """
        Locate the :class:`tornado.web.URLSpec` for ``cls``.

        :param class cls: the request handler class to look up
        :return: the URL spec route associated with the current
            request host and ``cls``
        :rtype: tornado.web.URLSpec
        :raises tornado.web.HTTPError: if no handler is found

        """
        for host_patn, host_handlers in self.application.handlers:
            if host_patn.match(self.request.host) is None:
                continue
            for urlspec in host_handlers:
                if urlspec.handler_class == cls:
                    return urlspec
        raise web.HTTPError(
            500, log_message='Failed to locate handler for {0}'.format(cls))

    @staticmethod
    def _build_path_args(urlspec, path_kwargs):
        """Build the path segment for a url using data from ``path_kwargs``

        :param tornado.web.URLSpec urlspec:
        :param dict path_kwargs:
        :return: the constructed relative path as a ``str``
        :raises tornado.web.HTTPError: if a path parameter from
            ``urlspec`` is not present in ``path_kwargs``

        """
        regex = urlspec.regex
        arg_list = [None for _ in range(regex.groups)]
        for arg_name, arg_index in regex.groupindex.items():
            try:
                arg_list[arg_index - 1] = path_kwargs.pop(arg_name)
            except KeyError:
                raise web.HTTPError(
                    500,
                    log_message='Path parameter {0} omitted'.format(arg_name),
                )
        return urlspec.reverse(*arg_list)

    @staticmethod
    def _rewrite_query(base_url, query_dict):
        """Replace the query portion of a URL.

        :param str base_url: the starting URL
        :param dict query_dict: the query parameters to insert
        :return: the newly minted URL
        :rtype: str

        """
        url_parts = compat.urlsplit(base_url)
        return compat.urlunsplit((
            url_parts.scheme,
            url_parts.netloc,
            url_parts.path,
            compat.urlencode(query_dict),
            None,  # fragment
        ))
