CHANGELOG
=========

List of release changes.

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
