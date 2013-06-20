# -*- coding: utf-8 -*-

# This file is subject to the terms and conditions defined in
# file 'LICENSE', which is part of this source code package.
#       Copyright (c) 2013 R Pratap Chakravarthy

from   os.path      import splitext, isfile, join
import os, tempfile

from   pluggdapps.plugin    import Plugin, implements
from   pagd.interfaces      import IContent


class Pandoc( Plugin ):
    """Plugin that can translate different content formats into html
    format. Under development, contributions are welcome.

    Make sure that pandoc tool is installed and available through shell
    command line interface. Supports reStructuredText and Markdown content
    formats.
    """
    implements( IContent )

    def __init__(self) :
        self.siteconfig = self['siteconfig'] if 'siteconfig' in self else {}
        self.cmd = join( os.environ['HOME'], '.cabal', 'bin', 'pandoc' )

    #---- IContent interface methods.

    def articles( self, page ):
        if not isfile(self.cmd) :
            raise Exception('Not found %r' % self.cmd)

        articles = []
        for fpath in page.contentfiles :
            if not isfile(fpath) : continue
            _, ext  = splitext(fpath)
            ftype = page.context.get('filetype', ext.lstrip('.'))
            metadata, content = self.parsers[ ftype ](self, fpath)
            articles.append( (fpath, metadata, content) )
        return articles

    def rst2html(self, fpath):
        return self.pandoc( self.cmd, fpath, 'rst', 'html' )

    def md2html(self, fpath):
        return self.pandoc( self.cmd, fpath, 'markdown', 'html' )

    def pandoc(self, cmd, fpath, fromm, to ):
        fd, tfile = tempfile.mkstemp()
        os.system(
                cmd + ' --highlight-style kate -f %s -t %s -o "%s" "%s"' % (
                      fromm, to, tfile, fpath) )
        return {}, open(fd).read()

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


