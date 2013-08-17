# -*- coding: utf-8 -*-

# This file is subject to the terms and conditions defined in
# file 'LICENSE', which is part of this source code package.
#       Copyright (c) 2013 R Pratap Chakravarthy

"""Collection of interfaces that can be stitch together to do static 
site-generation. Note that these interfaces are loosely defined and does not
impose a strict design for users. Almost always the design is enforced by
:class:`ILayout` plugins.
"""


from   pluggdapps.plugin    import Interface

class ILayout(Interface):
    """Interface to define layout and manage a static site."""

    sitepath = None
    """Path to directory where a new layout is created."""

    siteconfig = {}
    """Configuration parameters for layout under `sitepath`. Normally site
    configuration is stored as `config.json` under ``sitepath``."""

    def is_exist( sitepath ):
        """Is there a valid layout under `sitepath`. Returns a boolean."""

    def create( overwrite=False ):
        """Create a new layout under ``sitepath``. Subsequently users will add
        content under ``sitepath`` which can then be translated to static
        web-site. Corresponds directly with `create` sub-command from pagd
        command line script.
        """

    def generate( buildtarget, regen=True, srcfile=None ):
        """Generate static web site from source layout, specified by
        ``sitepath``. Corresponds directly with `gen` sub-command from pagd
        command line script.

        ``buildtarget``,
            Absolute directory path or directory path relative to `sitepath`
            where generated html site-pages are saved. Your static web site is
            available under buildtarget.

        ``regen``,
            If True regenerate all source files, whether modified or
            unmodified. Default is True.
        """

    def pages( sitepath ):
        """To build the static site from a source layout, first individual
        pages must be identified. This interface method iterates over each and
        every site-page that is identified under source layout. Refer to
        corresponding layout-plugin to know how pages are idenfitied from
        source layout.

        This is normally called during :meth:`generate`.
        
        For each iteration returns ``page`` object, which is an instance of
        class :class:`Page`.
        """

    def pagecontext(page):
        """After a page is identified, corresponding context information must
        be gathered. Context can be saved in JSON files that have one-to-one
        mapping with content-pages, and/or it can be supplied by the content
        itself (many markups, like rst, markdown, allow authors to add 
        meta-data in their document). Refer to corresponding layout-plugin to
        know how pages are idenfitied from source layout.

        Returns back dictionary of ``context`` attributes.
        """

    def pagecontent(page):
        """Read the page content from one or more files, specified by
        ``contentfiles`` attribute, and convert them into html articles.
        Normally content files are authored in plain text or using rst,
        markdown, or even raw html. Refer to corresponding :class:`IContent`
        plugin to know supported formats.

        Retun back list of ``articles``. Refer to :class:`Page` class to know
        the structure of article element.
        """

    def pagetemplate(page):
        """Locate the template file from the layout's template sub-directory
        and return the template file.
        
        ``page``,
            An instance of class :class:`Page`.

        Return template file as absolute file path. If False or None is
        returned then, either template file couldn't be located or not located
        for other reasons.
        """

    def newpage( pagename ):
        """Create a new content page in layout's source tree. Corresponds
        directly with `newpage` sub-command from pagd command line script.
        
        ``pagename``,
            name of the new file, that shall be interpreted as a new web-page
            for static web-site. Along with filename, file extension and file
            path is to be supplied. If one or both left unspecified then it is
            updo the layout-plugin to take a default action.
        """



class IContent(Interface):
    """Interface specification to compile text friendly content to
    web-friendly content. These contents will be supplied to page-templates
    during page generation.
    
    All methods of this plugin are re-entrant.

    ``siteconfig`` dictionary will be made available as plugin's settings key,
    access them as self['siteconfig'].
    """

    def articles( page ):
        """
        ``page``,
            An instance of class :class:`Page`. Attribute `contentfiles` is
            significant for this function.

        Interpret each content file and translate them into web friendly
        format that can be used by page-templates.

        Return a tuple of,
            ( article's fpath, dictionary-of-metadata, html-text ).

        Note that meta-data for each article will finally include context
        attributes from page's context json, default-json and even external
        context if supplied.
        """


class IXContext(Interface):
    """Interface specification to fetch page context from external sources.

    All methods of this plugin are re-entrant.

    ``siteconfig`` dictionary will be made available as plugin's settings key,
    access them as self['siteconfig'].
    """

    def fetch( page=None, article=None ):
        """Fetch the context from external source for page. Some times, if
        more than one article is present for a page, then instead of using
        ``page`` keyword, supply the ``article`` keyword.

        ``page``,
            an instance of class :class:`Page`. Contains page description and
            its context gathered so far.

        ``article``,
            a tuple of article content and metadata, refer to :class:`Page`
            for exact detail.

        Return a python dictionary of context attributes. Context must contain
        basic python data-types like integers, float, string, list, tuple,
        dictionary.
        """


class ITemplate(Interface):
    """Interface specification to translate a page using a template file.

    All methods of this plugin are re-entrant.

    ``siteconfig`` dictionary will be made available as plugin's settings key,
    access them as self['siteconfig'].
    """

    extensions = []
    """List of template file extensions that this plugin can parse."""

    def render( page ):
        """Render the final html page in the target site-directory."""


class IPublish(Interface):
    """Interface specification to publish generated site on the net or else
    where."""

    def publish( site ):
        """Publish the generated site on the net."""

