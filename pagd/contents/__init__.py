# -*- coding: utf-8 -*-

# This file is subject to the terms and conditions defined in
# file 'LICENSE', which is part of this source code package.
#       Copyright (c) 2013 R Pratap Chakravarthy

"""Contains a collection of plugins to parse content text from source layout
and generate html text for each page. The module also defines a collection of
library utilities that can be used by the plugins.
"""

import re

import pagd.contents.native     # Translate content in native python.
import pagd.contents.pandoc     # Translate content using pandoc, Haskell.

def rst2html(fpath, page):
    """``fpath`` is identified as a file containing ReStructured text. Read
    the file content, gather metadata from the content (if specified),
    translate content to HTML.

    And return a tuple of (metadata, content). Content is HTML text."""
    from docutils     import core, io, nodes

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


def md2html(fpath, page):
    """``fpath`` is identified as a file containing markdown text. Read
    the file content, gather metadata from the content (if specified),
    translate content to HTML.

    And return a tuple of (metadata, content). Content is HTML text."""
    from markdown     import Markdown
    
    md = Markdown( extensions=['meta'],
                   output_format='html5', safe_mode='escape' )
    content = md.convert( open(fpath).read() )
    metadata = {name.lower() : value[0] for name, value in md.meta.items()}
    return metadata, content


def html2html(fpath, page):
    """``fpath`` is identified as a file containing raw-html text. If html
    contains <meta> tag elements, it will be used as source of meta-data
    information.

    And return a tuple of (metadata, content). Content is HTML text."""
    html = open(fpath).read()
    metadata = html2metadata(html)
    return metadata, html


metare = re.compile(r':([a-zA-Z0-9_.-]+):(.+)')
def text2html(fpath, page):
    """``fpath`` is identified as a file containing plain text. If beginning
    of file contains text in the following format ::

        :<name>: <value>
        :<name>: <value>
        :<name>: <value>
    
    without any leading whitespace, it will be interpreted as meta-data and
    stripped off from the final text.

    Return a tuple of (metadata, content). Content is HTML text."""
    lines = open(fpath).read().splitlines()
    metadata = []
    while lines :
        if lines[0].startwith('    ') and metadata :
            metadata[-1][1] = metadata[-1][1] + ' ' + lines[0].lstrip(' ')
        try : name, value = metare.match(lines[0])
        except : break
        metadata.append( (name, value) )
        lines.pop()
    return dict(metadata), ('<pre>%s</pre>' % os.linesep.join( lines ))


def html2metadata(html):
    import lxml.html
    lxml.html.fromstring( html )
    metadata = {
        meta.attrib.get('name', None) : meta.attrib.get('content', None)
        for meta in root.xpath( '//meta' ) }
    return metadata
