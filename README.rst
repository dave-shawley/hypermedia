hypermedia
==========

*"REST APIs must be hypertext-driven"*, Roy T. Fielding

|Version| |Downloads| |Status| |License|

Wait... Why?
------------
The "Why" is pretty simple... there are an abundance of frameworks that
make things *RESTful* by generating deterministic URLs for your database
objects.  Then you implement the popular HTTP methods to provide a nice
way to interact with your newly minted resources.  Congratulations, you
have successfully mapped SQL into HTTP.  The URL has become your ``WHERE``
clause and ``PUT``, ``POST``, and ``GET`` are synonyms for ``UPDATE``,
``INSERT`` and ``SELECT``.

So that is a *very* tongue-in-cheek answer for *why did I feel the need
to write this library*.  However it is not a great answer nor even an
acceptable one in my opinion.  The *why* is much more nuanced than that.
The implementation that I just ranted about may indeed be quite RESTful
but we need to know more about a solution than its URL structure and how
it interprets various protocol actions before we can make that decision.
This isn't a dissertation on the Representation State Transfer
architectural principles, I leave that to `Dr. Fielding`_.  This library
attempts to provide a few mechanisms to make developing RESTful protocols
simpler.

.. Random notes for geeks that read the ReST source
.. "Hypermedia is defined by the presence of application control
.. information embedded within, or as a layer above, the presentation
.. of information." - Roy T. Fielding.
..
.. RFC-5988: Link Header
.. RFC-6570: URI Template

What?
-----
This library offers functionality that simplifies writing RESTful service
implementations over an existing HTTP server stack such as `Flask`_ or
`Tornado`_.  The HTTP stacks provide very clean and usable ways to
construct URLs and route HTTP requests to specific chunks of code.  I'm
not going to implement that again.  Instead, this library provides ways
to embed hypermedia controls into your responses without introducing lots
of nasty coupling in your application code.

This library is essentially an on-ramp to supporting Hypermedia Controls
in your HTTP application.  *Hypermedia Controls* referring to what is known
as Level 3 of the `Richardson Maturity Model`_.  This model was described
by Leonard Richardson at QCon in 2008 and has been further examined in
Jim Webber's most excellent `REST in Practice`_.  Here is a brief recap:

*Level Zero*

   One URL, one HTTP method - ``POST``.  Document describes the function
   to invoke, parameters, etc.  Response is the *return value*.

   *"There's a little web-based peephole into some other universe, and
   you can only communicate wit the other universe by passing messages
   through the peephole."* - L. Richardson.

*Level One: Resources*

   URLs identify resources but interactions are limited to sending a
   message that describes the function to invoke, parameters, etc.
   The interactions with different resources instances usually
   depend on URL patterns.

*Level Two: HTTP*

   Resources are still identified by constructed URLs but interactions
   follow the rules of HTTP with respect to its verbs (methods).  This
   is where most RESTful APIs stop.

*Level Three: Hypermedia Controls*
   
   This is where the seldom understood and inpronouncable term `HATEOAS`_
   shows up.  Instead of the URL being formulated by the user of the
   service based on what they want to do and some URL pattern syntax, the
   available actions are represented directly in the document as named
   links.  See `REST APIs must by hypertext-driven`_ for a
   well-written and relatively short rationale.

That is the part of the story that this library attempts to fill.  It
lets you write code like:

.. code-block:: python

   from hypermedia.tornado import mixins
   from tornado import web


   class PersonHandler(mixins.Linker, web.RequestHandler):
      
      def get(self, uid):
         person = get_person_information(uid)
         self.add_link('related-shows', SearchHandler, 'GET',
                       person_id=uid, type='shows')
         self.add_link('related-movies', SearchHandler, 'GET',
                       person_id=uid, type='movies')
         self.add_link('add-comment', CommentHandler, 'POST', uid=uid)
         self.add_link('comments', CommentHandler, 'GET', uid=uid)

         response = {}
         # ... build out the response
         response['links'] = self.get_link_map()

         self.write(response)

   class SearchHandler(web.RequestHandler):

      def get(self):
         # processes query parameters

   class CommentHandler(web.RequestHandler):

      def get(self, uid):
         # retrieve comments

      def post(self, uid):
         # add a comment

The ``hypermedia.tornado.mixins.Linker`` class takes care of constructing
the appropriate links based on the registered handlers and makes them
available via the ``get_link_map()`` method.

Ok... Where?
------------

+---------------+-------------------------------------------------+
| Source        | https://github.com/dave-shawley/hypermedia      |
+---------------+-------------------------------------------------+
| Status        | https://travis-ci.org/dave-shawley/hypermedia   |
+---------------+-------------------------------------------------+
| Download      | https://pypi.python.org/pypi/hypermedia         |
+---------------+-------------------------------------------------+
| Documentation | http://hypermedia.readthedocs.org/en/latest     |
+---------------+-------------------------------------------------+
| Issues        | https://github.com/dave-shawley/hypermedia      |
+---------------+-------------------------------------------------+

.. _Dr. Fielding: http://www.ics.uci.edu/~fielding/pubs/dissertation/top.htm
.. _Flask: http://flask.pocoo.org
.. _HATEOAS: http://www.slideshare.net/d0nn9n/jimwebber-rest
.. _REST APIs must by hypertext-driven: http://roy.gbiv.com/untangled/2008/rest-apis-must-be-hypertext-driven
.. _REST in Practice: http://www.amazon.com/gp/product/0596805829?ie=UTF8&tag=jimwebbesblog-20&linkCode=xm2&camp=1789&creativeASIN=0596805829
.. _Richardson Maturity Model: http://www.crummy.com/writing/speaking/2008-QCon/act3.html
.. _Tornado: http://tornadoweb.org

.. |Version| image:: https://pypip.in/version/hypermedia/badge.svg
   :target: https://pypi.python.org/pypi/hypermedia
.. |Downloads| image:: https://pypip.in/d/hypermedia/badge.svg
   :target: https://pypi.python.org/pypi/hypermedia
.. |Status| image:: https://travis-ci.org/dave-shawley/hypermedia.svg
   :target: https://travis-ci.org/dave-shawley/hypermedia
.. |License| image:: https://pypip.in/license/hypermedia/badge.svg
   :target: https://hypermedia.readthedocs.org/
