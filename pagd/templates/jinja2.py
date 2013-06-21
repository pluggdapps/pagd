# -*- coding: utf-8 -*-

# This file is subject to the terms and conditions defined in
# file 'LICENSE', which is part of this source code package.
#       Copyright (c) 2013 R Pratap Chakravarthy

from   pluggdapps.plugin        import Plugin, implements
import pluggdapps.interfaces

import pagd.interfaces

try    :
    from   jinja2 import Environment, FileSystemLoader
    class Jinja2( Plugin ):
        """Plugin to translate jinja2 templates to html files."""
        implements( pagd.interfaces.ITemplate )

        def __init__( self ):
            kwargs = {
                'loader'      : 
                    FileSystemLoader( self['sitepath'] ),
                'auto_reload' : 
                    self['siteconfig'].get('jinja2.auto_reload', False),
                'cache_size'  : 
                    self['siteconfig'].get('jinja2.cache_size', 50),
                'extensions'  :
                    self['siteconfig'].get('jinja2.extensions', ()),
            }
            self.env = Environment( **kwargs )

        def render( self, page ):
            return self._get_template( page.templatefile 
                                     ).render( page.context )

        def _get_template( self, template_name, globals=None ):
            return self.env.get_template(template_name, globals=globals)

except :
    pass

