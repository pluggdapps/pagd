# -*- coding: utf-8 -*-

# This file is subject to the terms and conditions defined in
# file 'LICENSE', which is part of this source code package.
#       Copyright (c) 2013 R Pratap Chakravarthy

from docutils import nodes
from docutils.parsers.rst import directives

CODE = """
    <script src="%s"></script>
"""

def gist( name, args, options, content, lineno,
             contentOffset, blockText, state, stateMachine ):
    """Restructured text extension for inserting github-gist embedded videos."""
    if content[0].startswith('http') :
        src = content[0]
    else : 
        src = 'https://gist.github.com/' + content[0].lstrip('/')
    return [ nodes.raw( '', CODE % (src), format='html')]

gist.content = True
directives.register_directive('gist', gist)
