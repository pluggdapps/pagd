# -*- coding: utf-8 -*-

# This file is subject to the terms and conditions defined in
# file 'LICENSE', which is part of this source code package.
#       Copyright (c) 2013 R Pratap Chakravarthy

from   pluggdapps.plugin        import Singleton, implements
from   pluggdapps.interfaces    import ICommand

from   pagd.interfaces          import ILayout

class Create( Singleton ):
    """Sub-command plugin to create a new layout at the given sitepath."""
    implements( ICommand )

    cmd = 'create'
    description = 'Create a source layout.'

    #---- ICommand API
    def subparser( self, parser, subparsers ):
        """:meth:`pluggdapps.interfaces.ICommand.subparser` interface method.
        """
        self.subparser = subparsers.add_parser( 
                                self.cmd, description=self.description )
        self.subparser.set_defaults( handler=self.handle )
        self.subparser.add_argument(
                '-f', '--force', dest='overwrite',
                action='store_true', default=False,
                help='Overwrite the source layout if it exists')
        return parser

    def handle( self, args ):
        """:meth:`pluggdapps.interfaces.ICommand.handle` interface method."""
        sett = { 'sitepath' : args.sitepath }
        layout = self.qp( ILayout, args.layout, settings=sett )
        if not layout :
            raise Exception(
                "The given layout is invalid. Please check if you have the "
                "`layout` in the right place and the environment variable "
                "has been setup properly if you are using custom path for "
                "layouts")
        if layout.is_exist() and not args.overwrite :
            raise Exception(
                "The given site path %r already contains a %r layout. "
                "Use -f to overwrite." % (args.sitepath, args.layout) )
        self.pa.loginfo(
            "Creating site at [%s] with layout [%s] ..." %
            (args.sitepath, args.layout))
        layout.create()
        self.pa.loginfo("... complete")

