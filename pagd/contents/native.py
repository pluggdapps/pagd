# -*- coding: utf-8 -*-

# This file is subject to the terms and conditions defined in
# file 'LICENSE', which is part of this source code package.
#       Copyright (c) 2011 R Pratap Chakravarthy

from os.path      import splitext, isfile

from   pluggdapps.plugin    import Plugin, implements
import pluggdapps.utils     as h
from   pagd.interfaces      import IContent


class Native( Plugin ):
    """Plugin that can translate different content formats into html
    format."""
    implements( IContent )

    def __init__(self) :
        # TODO : Create a parser object once and reuse them for all page
        # contents.
        pass

    #---- IContent interface methods.

    def articles( self, page ):
        articles = []
        for fpath in page.contentfiles :
            if not isfile(fpath) : continue
            _, ext  = splitext(fpath)
            ftype = page.context.get('filetype', ext.lstrip('.'))
            metadata, html = self.parsers[ ftype ](self, fpath)
            articles.append( (fpath, metadata, html) )
        return articles

    def rst2html(self, fpath):
        from docutils import core, io, nodes

        setts = { 'syntax_highlight': 'short' }
        pub = core.Publisher( destination_class=io.StringOutput )
        pub.set_components( 'standalone', 'restructuredtext', 'html' )
        pub.process_programmatic_settings(None, setts, None)
        pub.set_source( source_path=fpath )
        pub.publish()
        parts = pub.writer.parts
        metadata = {}
        for docinfo in pub.document.traverse(nodes.docinfo) :
            for element in docinfo.children :
                if element.tagname == 'field' : # Generic field
                    name, value = element.children
                    metadata[ name.astext().lower() ] = value.astext()
                else :  # Standard fields
                    metadata[ element.tagname.lower() ] = element.astext()
        content = parts.get('body')
        return metadata, content

    def md2html(self, fpath):
        # TODO : If page context has markdown configuration use them in the
        # Markdown() constructor.
        from markdown import Markdown
        md = Markdown( extensions=['meta'],
                       output_format='html5', safe_mode='escape' )
        content = md.convert( open(fpath).read() )
        metadata = {name.lower() : value[0] for name, value in md.meta.items()}
        return metadata, content

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
    }
