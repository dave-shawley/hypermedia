Reference
=========

Tornado Companions
------------------

.. autoclass:: hypermedia.tornado.mixins.Linker
   :members:

Flask Companions
----------------

The ``flask.ext.hypermedia`` extension incorporates hypermedia links
into a :class:`flask.Flask` instance.  It hooks itself into the Flask
routing mechanism and builds a map of advertised action name to endpoint
rule which you can query when you are building responses.

When adding routes with the :meth:`flask.Flask.route` decorator or
by calling :meth:`flask.Flask.add_url_rule`, you use the new ``advertise_as``
keyword parameter to specify the name of the action to associate with the
route.  This will cause the route and associated action name to be saved
by the :class:`flask_hypermedia.LinkMap` instance.

.. code-block:: python

    from flask.ext import hypermedia
    import flask

    app = flask.Flask(__name__)
    linker = hypermedia.LinkMap(app)

    @app.route('/', advertise_as='get-thingy')
    def getter():
        pass

    @app.route('/', advertise_as='add-thingy', methods=['POST'])
    def creator():
        pass

    @app.route('/<id>', advertise_as='put-thingy', methods=['PUT'])
    def setter(thingy_id):
        pass


Each rule that you advertise is available by name from the
:class:`flask_hypermedia.LinkMap` instance - ``linker`` in the previous
example.  Assuming the application above, the following snippet shows
what is available::

    >>> linker['get-thingy']
    {'rule': <Rule '/' (GET, OPTIONS, HEAD) -> getter>, 'method': 'GET'}
    >>> linker['add-thingy']
    {'rule': <Rule '/' (POST, OPTIONS) -> creator>, 'method': 'POST'}
    >>> with app.test_request_context('/'):
    ...    print(flask.url_for(linker['put-thingy']['rule'].endpoint, id=12))
    ...
    /12

.. autoclass:: flask_hypermedia.LinkMap
   :members:

Errors
~~~~~~

.. automodule:: flask_hypermedia.exceptions
   :members:
