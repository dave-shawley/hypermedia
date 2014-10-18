from flask.ext import hypermedia
from flask.ext.hypermedia import exceptions
import flask

from . compat import unittest


app = flask.Flask(__name__)
linker = hypermedia.LinkMap(app)


@app.route('/simple', advertise_as='get-simple')
def simple():
    pass


@app.route('/explicit', endpoint='explicit', advertise_as='get-explicit')
def explicit_function():
    pass


@app.route('/simple', methods=['PUT'], advertise_as='put-simple')
def make_it_simple():
    pass


class WhenFreeFunctionsAreDecorated(unittest.TestCase):

    def test_get_is_advertised_by_default(self):
        self.assertEqual(linker['get-simple']['method'], 'GET')
        self.assertEqual(linker['get-explicit']['method'], 'GET')

    def test_single_method_is_automatically_advertised(self):
        self.assertEqual(linker['put-simple']['method'], 'PUT')

    def test_that_correct_endpoints_are_advertised(self):
        self.assertEqual(linker['get-simple']['rule'].endpoint, 'simple')
        self.assertEqual(linker['get-explicit']['rule'].endpoint, 'explicit')
        self.assertEqual(linker['put-simple']['rule'].endpoint,
                         'make_it_simple')

    def test_that_multiple_methods_cannot_be_advertised(self):
        with self.assertRaises(exceptions.CannotDetermineMethod):
            @app.route('/fail1', methods=['1', '2'], advertise_as='busted')
            def fail1():
                pass

    def test_that_nonexistent_method_cannot_be_advertised(self):
        with self.assertRaises(exceptions.MethodDoesNotExist):
            @app.route('/fail2', advertise_as='busted', advertise_method='PUT')
            def fail2():
                pass

    def test_that_advertising_same_action_twice_fails(self):
        with self.assertRaises(exceptions.AlreadyAdvertised):
            @app.route('/fail3', advertise_as='get-simple')
            def fail3():
                pass
