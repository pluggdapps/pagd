# -*- coding: utf-8 -*-

# This file is subject to the terms and conditions defined in
# file 'LICENSE', which is part of this source code package.
#       Copyright (c) 2011 R Pratap Chakravarthy

from   os.path      import splitext, isfile

from   pluggdapps.plugin    import Plugin, implements
import pluggdapps.utils     as h
import pluggdapps.interfaces

from   pagd.interfaces      import IContent


class Native( Plugin ):
    """Plugin that can translate different content formats into html
    format using python native modules. Uses function APIs defined under
    :mod:`pagd.contents` module, except for ttl2html.

    Supports reStructuredText, Markdown, plain-text, plain-html,
    tayra-templates text.

    Note that in case of a TTL file, it is interpreted as page content and not
    as template for this or any other page-contents.
    """
    implements( IContent )

    def __init__(self) :
        self.siteconfig = self['siteconfig'] if 'siteconfig' in self else {}
        setts = h.settingsfor('tayra.ttlcompiler.', self.siteconfig)
        setts.update( debug=True )
        self.ttlplugin = self.qp(
                            pluggdapps.interfaces.ITemplate, 'tayra.TTLCompiler',
                            settings=setts )

    #---- IContent interface methods.

    def articles( self, page ):
        """For ``page``, an instance of :class:`Page` class, using its
        ``contentfiles`` attribute, translate each file's text to html and
        return a corresponding list of articles. Where each element in the
        article is a tuple of, ::

            ( article's fpath, dictionary-of-metadata, html-text )
        """

        articles = []
        for fpath in page.contentfiles :
            if not isfile(fpath) : continue
            _, ext  = splitext(fpath)
            ftype = page.context.get('filetype', ext.lstrip('.'))
            metadata, html = self.parsers[ ftype ](self, fpath, page)
            articles.append( (fpath, metadata, html) )
        return articles

    def rst2html(self, fpath, page):
        from pagd.contents  import rst2html
        return rst2html(fpath, page)

    def md2html(self, fpath, page):
        from pagd.contents  import md2html
        return md2html(fpath, page)

    def html2html(self, fpath, page):
        from pagd.contents  import html2html
        return html2html(fpath, page)

    def text2html(self, fpath, page):
        from pagd.contents  import text2html
        return text2html(fpath, page)

    def ttl2html(self, fpath, page):
        """``fpath`` is identified as a file containing tayra template text. If
        generated html contains <meta> tag elements, it will be used as source of
        meta-data information.

        And return a tuple of (metadata, content). Content is HTML text."""
        from pagd.contents  import html2metadata
        html = self.ttlplugin.render(page.context, file=fpath)
        metadata = html2metadata(html)
        return metadata, html


    parsers = {
        'rst' : rst2html,
        'markdown' : md2html,
        'mdown' : md2html,
        'mkdn' : md2html,
        'md' : md2html,
        'mkd' : md2html,
        'mdwn' : md2html,
        'mdtxt' : md2html,
        'mdtext' : md2html,
        'txt' : text2html,
        'text' : text2html,
        'html' : html2html,
        'htm' : html2html,
        'ttl' : ttl2html,
    }

