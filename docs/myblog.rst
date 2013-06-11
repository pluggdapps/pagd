directory structure
-------------------

One of the first thing a user must do is to create a site-layout using one of
the layout plugin - in this case `pagd.myblog`.

.. code-block:: bash

    pagd -s /home/me/blogsite -l pagd.myblog create

``-s`` switch specifies the directory path, also called as sitepath, where
the layout is created. If left unspecified sitepath defaults to
current-working-directory.

``-l`` switch specifies the layout plugin to be used for creating the site
layout. If left unspecified uses a default layout.

Refer to the glossary_ page before continuing further. The above command will
create following directory tree,

.. code-block::

    +- config.json
    +- _contents/
    |  +- _context.json
    |
    +- media/
    |  +- myblog.css
    |  +- pygments.css
    |
    +- _templates/
       +- _default.ttl
       +- _footer.ttl
       +- _header.ttl
       +- _head.ttl
       +- index.ttl

Following is the general idea on how `pagd.myblog` layout works, ::

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


Generator is normally called through `gen` sub-command, the sole purpose is to
generate the static site form a source layout, which is described above.

- generator iterates over every page under the _contents/ sub-directory.
- files under _contents/ sub-directory can further be organised as
  sub-directories and the relative path of each file will correspond to
  relative-url-path for generate page.
- each page is represented as :class:`Page` object and contains relevant
  information like, pagename, relative-path, urlpath, contentfiles and
  context.
- context for each page is populated using sub-directory's default-context,
  page's corresponding json file, page-metadata.
- page content is translated to html content using an `IContent` plugin.
- template for each page is searched under _template/ sub-directory using
  file's relative path. If file specific template is not found, then a default
  template from relative-path's parent sub-directory will be used.
- and finally the generated html will be saved under sitepath. Note that
  template and content authors must take this into account, especially when
  referring to files under media/ path.
  
configuration settings
----------------------
  
layout,
    layout type to be used, like e.g, ``pagd.myblog``.

tayra.ttlcompiler.*
    configuration parameters prefixed with ``tayra.ttlcompiler.`` will be
    passed on to Tayra template compiler.


context information
-------------------

  site
    :class:`Site` instance. Every page under the site will refer to the same
    `site` instance.

  page
    :class:`Page` instance.

  title
    Page title. Will be added under html <title> tag.

  layout
    layout type to be used. Same as `layout` parameter from configuration
    settings.

  last_modified
    modified time of the page, formated as "%a %b %d, %Y". Picked from
    file system's `mtime`.

  date
    Page created time. Can be specified as part of page-metadata or page's
    json context.

  _xcontext,
    Fetch the context from external source, like from network or from persistant
    data store.

  IContent,
    Plugin name for translating :class:`Page` to html. Plugins supplied with
    the package - `pagd.native`, `pagd.pandoc` etc ... if left un-specified
    then default plugin will be used. Most probably the default plugin is
    `pagd.native`.

  filetype,
    Interpret content-file as `filetype`. Note that if more than one contentfile
    is present for the same page, this settings will be ignored. If left
    un-specified, file extension will be used to guess its file-type.

  articles,
    List of tuple, (filepath, html-content), that can be used to populate the
    page-template during site-generation.

  template
    template location in asset-spefication format to be used for the
    content-page.

  templatetype,
    Interpret the template file as given type. If left unspecified template type
    will be guessed based on file extension.

