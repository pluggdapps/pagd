# -*- coding: utf-8 -*-

# This file is subject to the terms and conditions defined in
# file 'LICENSE', which is part of this source code package.
#       Copyright (c) 2013 R Pratap Chakravarthy

from docutils import nodes
from docutils.parsers.rst import directives

block = """
<div class="rst-gallery">
    <div class="gallery-title">%s</div>
    %s
</div>
"""
thumb = '<a href="%s" title="%s"><img src="%s"></img></a>'

def gallery( name, args, options, content, lineno,
             contentOffset, blockText, state, stateMachine ):
    """Restructured text extension for inserting youtube embedded videos."""
    s = ''
    title = content[0]
    for z in [ y.strip() for x in content[1:] for y in x.split(',') ] :
        try : src, imgtitle = z
        except : src, imgtitle = z, ''
        s += thumb % (src, imgtitle, src)
    return [ nodes.raw( '', block % (title, s), format='html')]

gallery.content = True
directives.register_directive('gallery', gallery)

