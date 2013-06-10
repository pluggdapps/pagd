General layout


Configuration
  
  layout,
    layout type to be used.

Content

        Gather context information from all `_context.json` files in the page
        path and finally override them with page's own context if available.

Context

  layout,
    layout type to be used. Same as config option `layout`.
  _xcontext,
    Fetch the context from external source, like from network or from persistant
    data store.
  IContent,
    Plugin name for translating :class:`Page` to html. Plugins supplied with
    the package - `pagd.native`, `pagd.pandoc`
  filetype,
    Interpret content-file as `filetype`. Note that if more than one contentfile
    is present for the same page, this settings will be ignored.
  articles,
    List of tuple, (filepath, html-content), that can be used to populate the
    page-template during site-generation.
  template
    template location in asset-spefication format to be used for the
    content-page.
  templatetype,
    Interpret the template file as given type. If left unspecified template type
    will be guessed based on file extension.
  site
    :class:`Site` instance
  page
    :class:`Page` instance


Template
