Static web site generator, based on well understood MVC - Model, View,
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
`github <https://github.com/prataprc/pagd>`_. Note that the orginal repository
is maintained with mercurial and uses hg-git plugin to publish it on github.

- **License:** `GPLv3 license <http://www.gnu.org/licenses/>`.
- **Requires:** Linux, Python-3.x, Pluggdapps.
- **Status:** Core design stable. Not expected to change.
