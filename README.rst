Overview
--------

Static web site generator, based on well understood MVC_ - Model, View,
Controller - design philosophy. The general idea behind MVC from web
application's perspective is

.. code-block:: text

                                      +--------+
                                      |template|
                                      +--------+
                                          |
                                          V   
           +-------+   +----------+    +------+    +-----+
           |request|-->|controller|--->|action|<---|model|
           +-------+   +----------+    +------+    +-----+
                                          |
                                          V
                                     +---------+
                                     |HTML page|
                                     +---------+
                                          |
                                          V
                goes to the client  +-------------+
              <---------------------|http-response|
                                    +-------------+


The general idea being that,

- http request reaches web-application's controller logic.
- controller resolves request to web-action by parsing request-URL.
- the action-logic gathers necessary context information from database models
  and other sources.
- a html-template is identified, and the final HTML page is generated using
  context information from models and page-layout from one or more template
  files.

``pagd`` follows, more or less, a similar principle to build a web-site from a
collection of files organised as a directory tree. Here is a brief idea on how
it is done

.. code-block:: text


       +------+    +---------+      +-------------+
       |layout|--->|generator|<---->|page-iterator| 
       +------+    +---------+      +-------------+
                        |                  ^
                        |                  |          +------------+
                        V                  +<---------|page-context|
                   +---------+             |          +------------+
                   |Html-page|             |       
                   +---------+             |          +-------------+
                        |                  +<---------|page-template|
                        |                  |          +-------------+
                        V            +------------+
                   +--------+        |page-content|
                   |web-site|        +------------+
                   +--------+      


Features
--------

- generates static output, hence can be hosted anywhere.
- pluggable layouts.

  - I am currently using `pagd.myblog` layout for publishing my blog articles.
  - It is possible to create any number of layout either as part of `pagd`
    tool or as separate package.
  - although layouts are encouraged to follow the Model-View-Controller
    concept explained above, it is up to the layout-plugin to define a structure
    and meaning of layout's source directory-tree.

- everything that needs to get done by pagd is done through ``pagd`` command
  line interface.
- command line interface comes with simple sub-commands like,

  - `create`, to create a new layout.
  - `gen`, to generate static web site from a source layout.

- sub-commands are plugins and can be extended by implementing
  pagd.interfaces.ICommand interface.
- to use pagd as python library, refer to ``script.py`` module under pagd
  package.
- web-site templates can be designed using `tayra template`_.

  - experimental feature is available for mako and jinja2. If you face problems
    with these templates, kindly let me know.

- reStructuredText directives,
  
  - code syntax highlighting.
  - play youtube video within page content.
  - display collection of images as gallery, uses magnific-popup_ jquery
    plugin. Magnific-popop is a well documented jquery plugin, it is possible
    to change its CSS file and/or pagd template script to customize it in 
    many ways.
  - to embed github gist, entire gist or individual file in a gist.

- ``pagd.myblog`` layout is loaded with batteries.

  - write blog articles in reStructured text, markdown, plain-text, html or
    even as tayra-templates.
  - template your site using tayra templates.
  - configure site generation using JSON file.
  - add context to individual pages are all pages under a sub-directory
    through one or more JSON files.
  - use google-webfonts_ by configuring CSS links using `config.json` attribute
    `google_webfonts`.
  - integration with disqus commenting system. Comments will be stored in
    disqus' server.
  - integration with git, mercurial repository to gather file's meta-data like
    page's author, email, created-time, last-modified-time etc..., this is
    entirely optional.
  - social sharing with twitter, facebook, hackernews, google+, reddit,
    linkedin etc...
  - includes jquery, template can be customized with jquery plugins.
  - learn more - pagd.myblog_.

- only part that cannot be configured, customized or entirely replaced, is
  the name of the tool ;)

- **License:** `GPLv3 license`_
- **Requires:** Linux, Python-3.x, Pluggdapps.

  - To interpret markdown text, python-markdown_ needs to be installed.
  - To interpret rst text, docutils_ needs to be installed.
  - To interpret raw-html, python-lxml_ needs to be installed.
  - If you need source code highlighting in your rst text, pygments_ and
    docutils_ needs to be installed.
  - To template with jinja2 or mako corresponding packages need to be
    installed.

- **Status:** Core design stable. Not expected to change.

Refer to glossary_ and documentation for default layout pagd.myblog_.

Related links
-------------

* `package documentation`_.
* changelog_.
* todo_.
* mailing-list_ - if you have any problem just ask !!

pagd is under development - you can hack the code, contribute back with
`github <https://github.com/prataprc/pagd>`_. Note that the original
repository is maintained with mercurial and uses hg-git plugin to publish it
on github.

.. _MVC: http://en.wikipedia.org/wiki/Model-view-controller
.. _GPLv3 license:  http://www.gnu.org/licenses/
.. _python-markdown: https://pypi.python.org/pypi/Markdown
.. _docutils: https://pypi.python.org/pypi/docutils
.. _pygments: https://pypi.python.org/pypi/pygments
.. _python-lxml: https://pypi.python.org/pypi/lxml
.. _google-webfonts: http://www.google.com/fonts
.. _magnific-popup: https://github.com/dimsemenov/Magnific-Popup

.. _tayra template: http://pythonhosted.org/tayra
.. _pagd.myblog: http://pythonhosted.org/pagd/myblog.html
.. _glossary: http://pythonhosted.org/pagd/glossary.html
.. _package documentation: http://pythonhosted.org/pagd
.. _changelog: http://pythonhosted.org/pagd/CHANGELOG.html
.. _todo: http://pythonhosted.org/pagd/TODO.html
.. _mailing-list: http://groups.google.com/group/pluggdapps
