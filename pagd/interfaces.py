# -*- coding: utf-8 -*-

# This file is subject to the terms and conditions defined in
# file 'LICENSE', which is part of this source code package.
#       Copyright (c) 2013 R Pratap Chakravarthy

from   pluggdapps.plugin    import Interface

class ILayout(Interface):
    """Interface to define layout and manage a static site."""

    sitepath = None
    """Path to directory where a new layout created."""

    siteconfig = {}
    """Configuration parameters for layout under `sitepath`."""

    def issite( sitepath ):
        """Is there a valid layout under `sitepath`. Returns a boolean."""

    def create():
        """Create a new copy of layout as site source."""

    def generate(buildtarget, **kwargs):
        """Generate static web site from source layout.

        ``buildtarget``,
            Absolute directory path or directory path relative to `sitepath`
            where generated html site-pages must be saved.

        kwargs can be,

        ``regen``,
            If True regenerate all source files, whether modified or
            unmodified.
        """

    def newpage():
        """Create a new content page in layout's source tree."""

    def pages( sitepath ):
        """For site under `sitepath`, return an iterator iterating over every
        page under the site. To be called during :meth:`generate`.
        
        For each iteration returns ``page`` object, which is an instance of
        class :class:`Page`.
        """

    def pagecontext(page):
        """Gather context information from all `_context.json` files in the page
        path and finally override them with page's own context if available.

        Returns back the page object with its ``context`` attribute updated
        with relevant context values.
        """

    def pagecontent(page):
        """Read the page content from one or more files, specified by
        ``contentfiles`` attribute, and convert them into html articles.

        Retun back the page object with its ``articles`` attribute updated
        with list of html text.
        """

    def pagetemplate(page):
        """Locate the template file from the layout's template sub-directory
        and return the template file.
        
        Return template file as absolute file path.
        """

    def pagegenerate(page):
        """Generate a html web page corresponding to content-page. Return
        html text for page.

        ``page``,
            An instance of class :class:`Page`.
        """


class IContent(Interface):
    """Interface specification to compile text friendly content to
    web-friendly content. These contents will be supplied to page-templates
    during page generation."""

    def articles( page ):
        """
        ``page``,
            An instance of class :class:`Page`. Attribute `contentfiles` is
            significant for this function.

        Interpret each content file and translate them into web friendly
        format that can be used by page-templates.

        Return a tuple of,
            ( article's fpath, dictionary-of-metadata, html-text ).
        """


class IXContext(Interface):
    """Interface specification to fetch page context from external sources."""

    def fetch( page ):
        """Fetch the context from external source for page.

        ``page``,
            an instance of class :class:`Page`. Contains page description and
            its context gather so far.

        Return a python dictionary of context attributes. Context must contain
        basic python data-types like integers, float, string, list, tuple,
        dictionary.
        """

class ITemplate(Interface):
    """Interface specification to translate a page using a template file."""

    def render( page ):
        """Render the final html page in the target site-directory."""


class IPublish(Interface):
    """Interface specification to publish generated site on the net or else
    where."""

    def publish( site ):
        """Publish the generated site on the net."""

