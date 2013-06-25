Myblog layout plugin
===================

This article explains myblog layout.

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

.. code-block:: text

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
       +- _social.ttl
       +- _social/
          +- disqus.html


- ``config.json`` contains a dictionary of settings that will direct pagd
  command like script. Individual settings parameter are explained further
  down.

- ``_context.json`` context information that are applicable to all pages and
  pages under all sub-directories.

- ``myblog.css`` style customization can be done through this file.

- ``_default.ttl`` template will be used for all other pages, if a matching
  template is not found for a page under _contents/ sub-directory.

- ``_footer.ttl`` constitute the footer portion of site pages. You can add
  acknowledgments, copyright notice under this template.

- ``_header.ttl`` constitute the header portion of site pages. You can add your
  site-wide navigation links inside this template file.

- ``_head.ttl`` will go under <head> element of the page. Both index.ttl and
  _default.ttl templates include them.

- ``index.ttl`` directly maps to ``_contents/index.<format>`` file. This
  template is used only for the index-page.

- ``_social.ttl`` adds social sharing features for your site. Uses
  `social_sharing` configuration parameter from `config.json`.

- ``_social/`` add all html snippets that you obtain from disqus, twitter,
  facebook etc... under this directory.

Following is the general idea on how `pagd.myblog` layout works,

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
  
external context
----------------

_context.json files providing context information for all pages under the
sub-directory or <pagename.json> files providing context attributes
to specific pages can refer to external source of context through `_xcontext`
attributes. Value of this attribute is a comma separated list of plugin names,
in canonical format like `pagd.git`, that refer to IXContext plugins. While
generating the site such references will be fetched and page's context
dictionary will be updated.

Repository integration is accomplished using this feature.

configuration settings
----------------------
  
  layout,
    layout type to be used, like e.g, ``pagd.myblog``.
  
  tayra.ttlcompiler.*
    configuration parameters prefixed with ``tayra.ttlcompiler.`` will be
    passed on to tayra_ template compiler.
  
  google_webfonts
    list of, comma-separated, google's webfonts reference. Refer to 
    google-webfonts_ on how to add web-fonts from google's site.
  
  style
    property map of css style that will be applied on page's body element.
  
  show_email
    boolean, if true will added email reference to page's author.
  
  social_sharing
    list of, comma-separated, string of social-networks that can be used to
    share a page. For eg., ``google+,twitter``, for each social network that are
    mentioned you must add a corresponding `twitter.html`, `google+.html`
    under ``_templates/_social/`` directory.
  
  disqus
    boolean, if true will add commenting system for the page using an external
    commenting service like disqus. Make sure to populate
    ``_templates/disqus.html`` file with a corresponding snippet.
  
  skip_context
    list of, comma-separated, context attribute names that should be skipped
    for all pages.

  copyright,
    copyright string that will be displayed in page footer.

configuration settings like ``disqus``, ``show_email``, ``social_sharing``,
``copyright``, ``google_webfonts``, ``style`` are automatically made available
in page-context.

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

  author
    name of page's author.

  email
    author's email-id.

  last_modified
    page's last modified time.

  createdon / date
    page creation time.

  _xcontext,
    comma separated string of plugin names (in canonical format) to fetch page
    context from external source, like from repository, network or from
    persistent data store.

  IContent,
    plugin name for translating :class:`Page` to html. Plugins supplied with
    the package - `pagd.native`, `pagd.pandoc` etc ... if left unspecified
    then default plugin will be used. Most probably the default plugin is
    `pagd.native`.

  filetype,
    interpret content-file as `filetype`. Note that if more than one contentfile
    is present for the same page, this settings will be ignored. If left
    un-specified, file extension will be used to guess its file-type.

  articles,
    list of tuple, (filepath, html-content), that can be used to populate the
    page-template during site-generation.

  template
    template location in asset-specification format to be used for the
    content-page.

  templatetype,
    interpret the template file as given type. If left unspecified template type
    will be guessed based on file extension.

.. _google-webfonts: http://www.google.com/fonts
.. _tayra: http://pythonhosted.org/tayra
