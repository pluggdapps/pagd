CHANGELOG
=========

List of release changes.

0.21dev
-------

``Wed Jan 05, 2014``

- migrated from mercurial to git repository, and the project is now tracked in
  github.
- rst plugin to embed gist file is added.
- configuration settings like ``disqus``, ``show_email``, ``social_sharing``,
  ``copyright``, ``google_webfonts``, ``style`` are automatically made
  available in page-context.
- ITemplate, IXContext, IContent plugins are instantiated by layout using the
  newly added ``plugin()`` library function.
- Support ``summary`` metadata for articles. It must be rendered below the
  title.
- age()-scale is calculated statically, so it does not make sense if the site
  is going to be generated once in a while. On the other hand if the site is
  going to be generated periodically, then corresponding scale-factor can be
  choosen by user.
- Styling for TOC.
- default configuration file config.json.
- updated CSS for myblog layout.


0.2dev
------

``Wed Jun 22, 2013``

- added youtube directive for reStructured Text,
  added image-gallery directive for rst using maginific-popup jquery plugin.
  created a `pagd.rst` sub-package, that contains reStructured text
  directives - sourcecode, youtube, gallery.

- any number of google webfonts can be referenced for every blog-page.

- added social-sharing feature to `pagd.myblog` layout.
  Social sharing templates are added under `_templates/_social/` directory.
  Right now supports twitter, disqus, hackernews, reddit, linkedin, google+
  and facebook.  `disqus.html` can contain disqus plugin. And other social
  plugins referred by "social_sharing" configuration option has `html` file
  under _template/_social/ directoy by the same name.
  For Eg, if social_sharing is `twitter,hn`, then users must generate their
  plugins snippets and save them under files `_templates/_social/twitter.html`
  and `_templates/_social/hn.html` respectively.

  social plugins also have CSS styling under myblog.css.

- Integration with git and hg through `IXContext` interface, fetches page meta
  information like, author, emailid, created-date, modified date etc .. from
  repository.

- ``pagd.git`` and ``pagd.hg`` plugins will use "day" scale while calculating
  last modified time for every article.

- added jquery link.

- moved "style", "google_webfonts", "copyright" out of _context.json to
  config.json. Felt that these attributes are more like configuration
  attributes than context attributes. Since templates can access the config
  dictionary as `page.site.siteconfig`, this does not cripple them.

- myblog pages contain only one article.

- blog pages have `author-name`, `created-time`, `last-modified-time` and
  `author's email reference`. Any or all of them can be disabled through
  ``config.json``.

- skip_context configuration option added using config.json. Using this it is
  possible to restrict usage of context information from `_contents/`.
  skip_context makes context attribute refer to None.

- CSS style blocks are added in `media/myblog.css`, meaningful comments added
  to myblog.css. Prefixes CSS id names with myblob- for pagd.myblog layout.

- Added a helper module ``pagd.h`` to contain helper functions for tayra
  templates. All functions inside this module will automatically be made
  available under ``h`` namespace inside ttl-script.

- Changed fetch() interface method for `IXContext` interface. Reasoning behind
  this is that, IXContext plugin's fetch() method can be called for entire page
  or for every article for this page.

- template plugins must be included under try ... except blocks to avoid
  crashing when they are not being used.

- removed duplicate dependencies.

- minor fixes in error logging and documentation

- Source documentation, using sphinx, is updated.

- pagd.myblog layout show email-id by default.


0.11dev
------

``Wed Jun 12, 2013``

- Added disqus plugin for pagd.myblog plugin. Can be enabled in config.json.
- Experimental support for mako and jinja2 templates.

0.1dev
------

``Tue Jun 11, 2013``

- generates static output, hence can be hosted anywhere.

- pluggable layouts.

- I am currently using `pagd.myblog` layout for publishing my blog articles.

- It is possible to create any number of layout either as part of `pagd`
  tool or as separate package.

- although layouts are encouraged to follow the Model-View-Controller
  concept explained above, it is entire upto the layout-plugin to define
  structure and meaning of source directory-tree.

- everything that needs to get done by pagd is done through ``pagd`` command
  line interface.

- command line interface comes with simple sub-commands like,

- `create`, to create a new layout.

- `gen`, to generate static web site from a source layout.

- sub-commands are plugins and can be extended by implementing
  pagd.interfaces.ICommand interface.

- to use pagd as python library, refer to ``script.py`` module under pagd
  package.

- only part that cannot be configured, constumized or entirely replaced, is
  the name of the tool ;)
