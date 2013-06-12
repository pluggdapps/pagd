# -*- coding: utf-8 -*-

# This file is subject to the terms and conditions defined in
# file 'LICENSE', which is part of this source code package.
#       Copyright (c) 2013 R Pratap Chakravarthy

from   pluggdapps.plugin        import implements, Singleton
from   pluggdapps.interfaces    import ICommand
import pluggdapps.utils         as h

class Commands( Singleton ):
    """Subcommand plugin for pa-script to list all available sub-commands 
    along with a short description. Like,
    
    .. code-block:: bash
        :linenos:
        
        $ pagd commands

    """

    implements( ICommand )

    description = 'list of script commands and their short description.'
    cmd = 'commands'

    #---- ICommand API
    def subparser( self, parser, subparsers ):
        """:meth:`pluggdapps.interfaces.ICommand.subparser` interface method.
        """
        self.subparser = subparsers.add_parser( 
                                self.cmd, description=self.description )
        self.subparser.set_defaults( handler=self.handle )

    def handle( self, args ):
        """:meth:`pluggdapps.interfaces.ICommand.handle` interface method."""
        commands = self.qpr(ICommand, 'pagd.*')
        commands = sorted( commands, key=lambda x : x.caname )
        for command in commands :
            name = command.caname.split('.', 1)[1]
            rows = self._formatdescr( name, command.description )
            for r in rows : print(r)

    #---- Internal & local functions
    def _formatdescr( self, name, description ):
        fmtstr = '%-' + str(self['command_width']) + 's %s'
        l = self['description_width']

        rows, line = [], ''
        words = ' '.join( description.strip().splitlines() ).split(' ')
        while words :
            word = words.pop(0)
            if len(line) + len(word) >= l : 
                rows.append( fmtstr % (name, line) )
                line, name = word, ''
            else :
                line = ' '.join([ x for x in [line,word] if x ])
        rows.append( fmtstr % (name, line) ) if line else None
        return rows

    #---- ISettings interface methods

    @classmethod
    def default_settings( cls ):
        """:meth:`pluggdapps.plugin.ISettings.default_settings` interface 
        method."""
        return _default_settings

    @classmethod
    def normalize_settings( cls, settings ):
        """:meth:`pluggdapps.plugin.ISettings.normalize_settings` interface 
        method."""
        settings['description_width'] = h.asint(settings['description_width'])
        settings['command_width'] = h.asint(settings['command_width'])
        return settings


_default_settings = h.ConfigDict()
_default_settings.__doc__ = Commands.__doc__

_default_settings['command_width']  = {
    'default' : 15,
    'types'   : (int,),
    'help'    : "Maximum width of command name column."
}
_default_settings['description_width']  = {
    'default' : 60,
    'types'   : (int,),
    'help'    : "Maximum width of description column."
}
