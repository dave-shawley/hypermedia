from tornado import httpserver, web

from hypermedia import compat
from hypermedia.tornado import mixins

from . compat import mock, unittest


class MovieHandler(mixins.Linker, web.RequestHandler):
    pass


class SearchHandler(web.RequestHandler):
    pass


class CommentHandler(web.RequestHandler):
    pass


app = web.Application([
    (r'/comments/(?P<uid>\d+)', CommentHandler),
    (r'/movie/(?P<uid>\d+)', MovieHandler),
    (r'/search', SearchHandler),
])
app.add_handlers(r'98\.139\.180\.149', [
    (r'/yahoo/(?P<uid>\d+)', CommentHandler),
])
app.add_handlers(r'65\.199\.32\.155', [
    (r'/google/(?P<uid>\d+)', CommentHandler),
])


def create_request(method, uri, headers=None):
    # Setting X-Forwarded-For is necessary to make our tests
    # work well with Tornado 3.x.  In 3.x, the remote_ip keyword
    # to HTTPRequest
    context = mock.Mock(remote_ip='172.16.0.1', protocol='http')
    request_headers = {'X-Forwarded-For': '172.16.0.1'}
    if headers is not None:
        request_headers.update(headers)
    return httpserver.HTTPRequest(
        method=method,
        uri=uri,
        connection=mock.Mock(context=context),
        headers=request_headers,
    )


class WhenCreatingLinker(unittest.TestCase):

    def setUp(self):
        super(WhenCreatingLinker, self).setUp()
        self.linker = mixins.Linker()

    def test_that_request_attribute_is_created(self):
        self.assertIsNone(self.linker.request)

    def test_that_application_attribute_is_created(self):
        self.assertIsNone(self.linker.application)


class WhenCreatingLinkerMixedInOverRequestHandler(unittest.TestCase):

    def setUp(self):
        super(WhenCreatingLinkerMixedInOverRequestHandler, self).setUp()
        self.request = create_request('GET', '/')
        self.linker = MovieHandler(app, self.request)

    def test_that_request_is_preserved(self):
        self.assertIs(self.linker.request, self.request)

    def test_that_application_is_preserved(self):
        self.assertIs(self.linker.application, app)


class WhenAddingSimpleLink(unittest.TestCase):

    def setUp(self):
        super(WhenAddingSimpleLink, self).setUp()
        self.handler = MovieHandler(
            app, create_request('GET', '/movie/1',
                                headers={'Host': '10.0.0.1:8080'}))
        self.handler.add_link('comments', CommentHandler, 'GET', uid=1)

    @property
    def generated_link(self):
        return self.handler.get_link_map()['comments']

    def test_that_link_includes_method(self):
        self.assertEquals(self.generated_link['method'], 'GET')

    def test_that_link_includes_absolute_url(self):
        self.assertEqual(self.generated_link['url'],
                         'http://10.0.0.1:8080/comments/1')


class WhenAddingQueryLink(unittest.TestCase):

    def setUp(self):
        super(WhenAddingQueryLink, self).setUp()
        self.handler = MovieHandler(app, create_request('GET', '/movie/1'))
        self.handler.add_link('find-actors', SearchHandler, 'GET', query={
            'movie': '/movie/1', 'search-for': 'actors',
        })

    @property
    def generated_link(self):
        return compat.urlsplit(
            self.handler.get_link_map()['find-actors']['url'])

    def test_that_link_path_is_correct(self):
        self.assertEqual(self.generated_link.path, '/search')

    def test_that_query_params_are_passed(self):
        self.assertEqual(
            compat.parse_qs(self.generated_link.query),
            {'search-for': ['actors'], 'movie': ['/movie/1']},
        )


class WhenAddingLinkToNonexistentHandler(unittest.TestCase):

    def setUp(self):
        super(WhenAddingLinkToNonexistentHandler, self).setUp()
        self.handler = MovieHandler(app, create_request('GET', '/movie/1'))

    def test_that_internal_error_is_raised(self):
        with self.assertRaises(web.HTTPError):
            self.handler.add_link('whaeva', web.RequestHandler, 'GET')


class WhenAddingLinkFromSpecificVirtualHost(unittest.TestCase):

    def setUp(self):
        super(WhenAddingLinkFromSpecificVirtualHost, self).setUp()
        self.handler = MovieHandler(
            app, create_request('GET', '/movie/1',
                                headers={'Host': '65.199.32.155'}))
        self.handler.add_link('add-comment', CommentHandler, 'POST', uid=1)

    def test_that_generated_link_has_correct_host(self):
        generated_link = compat.urlsplit(
            self.handler.get_link_map()['add-comment']['url'])
        self.assertEqual(generated_link.netloc, '65.199.32.155')


class WhenAddingLinkWithMissingParameter(unittest.TestCase):

    def setUp(self):
        super(WhenAddingLinkWithMissingParameter, self).setUp()
        self.handler = MovieHandler(app, create_request('GET', '/movie/1'))

    def test_that_internal_error_is_raised(self):
        with self.assertRaises(web.HTTPError):
            self.handler.add_link('add-comment', CommentHandler, 'POST')
