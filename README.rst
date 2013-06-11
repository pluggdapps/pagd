Static web site generator, based on well understood MVC_ - Model, View,
Controller - design philosophy. The general idea behind MVC from web
application's perspective is ::

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
it is done ::


       +------+    +---------+      +-------------+
       |layout|--->|generator|<---->|page-iterator| 
       +------+    +---------+      +-------------+
                        |                  ^
                        |                  |          +------------+
                        V                  *<---------|page-context|
                   +---------+             |          +------------+
                   |Html-page|             |       
                   +---------+             |          +-------------+
                        |                  *<---------|page-template|
                        |                  |          +-------------+
                        V            +------------+
                   +--------+        |page-content|
                   |web-site|        +------------+
                   +--------+      


``pagd`` core-design is stable. Some plugins, that are shipped along ``pagd``
package are not fully tested - you can hack the code, contribute back with
`github_ <https://github.com/prataprc/pagd>`_. Note that the orginal repository
is maintained with mercurial and uses hg-git plugin to publish it on github.

- generates static output, hence can be hosted anywhere.
- pluggable layouts.

  - I am currently using `pagd.myblog` layout for publishing my blog articles.
  - It is possible to create any number of layout either as part of `pagd`
    tool or as separate package.

- everything that needs to get done by pagd is done through ``pagd`` command
  line interface.
- command line interface comes with simple sub-commands like,

  - `create`, to create a new layout.
  - `gen`, to generate static web site from a source layout.

- sub-commands are plugins and can be extended by implementing
  pagd.interfaces.ICommand interface.
- 
- to use pagd as python library, refer to ``script.py`` module under pagd
  package.
- only part that cannot be configured, constumized or entirely replaced, is
  the name of the tool ;)

- **License:** `GPLv3 license`_
- **Requires:** Linux, Python-3.x, Pluggdapps.
    - To interpret markdown text, python-markdown_ needs to be installed.
    - To interpret rst text, docutils_ needs to be installed.
    - To interpret raw-html, python-lxml_ needs to be installed.
    - If you need source code highlighting in your rst text, ``pygments`` and
      ``docutils`` needs to be installed.
- **Status:** Core design stable. Not expected to change.

.. _MVC: http://en.wikipedia.org/wiki/Model-view-controller
.. _GPLv3 license:  http://www.gnu.org/licenses/
.. _python-markdown: https://pypi.python.org/pypi/Markdown
.. _docutils: https://pypi.python.org/pypi/docutils
.. _python-lxml: https://pypi.python.org/pypi/lxml

