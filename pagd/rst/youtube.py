# -*- coding: utf-8 -*-
# This code is from http://countergram.com/youtube-in-rst

from docutils import nodes
from docutils.parsers.rst import directives

CODE = """\
<object class="rst-youtube" type="application/x-shockwave-flash"
        %(attrs)s data="http://www.youtube.com/v/%(yid)s">
    <param name="movie" value="http://www.youtube.com/v/%(yid)s"></param>
    <param name="wmode" value="transparent"></param> %(extra)s
</object>
"""

PARAM = """\n<param name="%s" value="%s"></param>"""

def youtube( name, args, options, content, lineno,
             contentOffset, blockText, state, stateMachine ):
    """Restructured text extension for inserting youtube embedded videos."""
    if len(content) == 0 : return
    string_vars = { 'yid': content[0],
                    'attrs': '',
                    'extra': ''
                  }
    attrs = content[1:] # Because content[0] is ID
    attrs = [attr.strip() for attr in content[1:]] # key=value
    string_vars['attrs'] = " ".join(attrs)
    return [ nodes.raw( '', CODE % (string_vars), format='html')]

youtube.content = True
directives.register_directive('youtube', youtube)
