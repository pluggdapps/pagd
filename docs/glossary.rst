Following is a glossary of terms that have special meaning under ``pagd`` and
more specifically pagd's ``myblog`` layout. In general, other layout plugins
are encouraged to be consistent with ``myblog`` layout's design concepts.

.. _glossary:

Glossary
========

.. glossary::
  :sorted:

  static-web-site
    A static web site in the context of `pagd` is a collection of html, css,
    javascript and other web-files (interpretable by browser like medium). The
    static site is generated from a source tree containing a collection of
    template, content and context for each page.
  
  layout 
    Contains source tree to generate static web site. A layout typically
    contains a source tree of page contents, associated context attributes for
    each page, collection of templates and a collection of media / web files.
  
    Layouts are implemented as plugins, like ``pagd.myblog``, that directly
    interfaces with sub-commands from command-line-interface (CLI). Most
    commonly used sub-commands are ``create`` to create a source tree of new
    layout, ``gen`` to generate a static web-site from layout source tree.
  
  sitepath
    Directory path containing a `pagd` layout.
  
  siteconfig
    A json file typically stored as `config.json` under `sitepath`. This file
    is parsed for configuration settings that will be applied during site
    generation. To learn more about available configuration settings refer to
    corresponding layout definition.
  
  content-page
    Content provides the main content for each page. Content can be organized
    as files and directories where the relative path to a content-file will
    directly correspond to relative-url-path in the generated web-site. Content
    files can be many formats like plain-text, re-structured text, one of the
    many wiki-markups like markdown, html etc ...
  
  context
    Every page content can have associated context description. For eg, let us
    say there is a content-page called `mycompany/contactus.md` containing a
    description of company location. Context can be associated to this page by
    describing them in a file, `mycompany/contactus.json`.
  
    Note that context information for each and every page can be stored in a
    corresponding `<pagename>.json` file.

    If content page, for eg. rst, markdown, html, supports metadata
    information as part of the page content, then the metadata found as part
    of page-content will override page-context from other sources.
  
  default-context
    It is possible to associate a set of context attributes for all 
    content-pages under a subdirectory. For eg, context attributes in 
    `mycompany/_context.json` will be associted with all content-pages under
    subdirectory `mycompany/`.
  
    Note that _context.json under a sub-directory will be associated with
    content-pages under the sub-directory tree. Attributes described in
    _context.json file are overridable by _context.json file described further
    down under sub-directories. And finally context attributes that are
    directly associted with content-page will override default-context.
  
  template
    While generating a web-site, every content-page under the source-layout 
    will be translated to corresponding web-page. The site generation process
    will pick up a template from its layout-source, and pass the page-content
    and page-context to the template. Templates can be described using tayra,
    mako, jinja2 and many other templating language. Refer to the
    corresponding layout and templating documentation to learn more about
    organizing templates for page generation.
  
  media
    Media files will be copied as it is to the target site. Interpretation of
    media files are left to layout plugins, hence refer to corresponding layout
    documentations for more information.
  
  cache
    Layouts can cache the site generation process to speed up performance. For
    more information refer to corresponding layout plugin.
  
