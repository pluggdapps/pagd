# -*- coding: utf-8 -*-

# This file is subject to the terms and conditions defined in
# file 'LICENSE', which is part of this source code package.
#       Copyright (c) 2013 R Pratap Chakravarthy

from   os.path                  import join, isfile

from   pluggdapps.plugin        import Singleton, implements
from   pluggdapps.interfaces    import ICommand

from   pagd.lib                 import json2dict
from   pagd.interfaces          import ILayout

class Create( Singleton ):
    """Sub-command plugin to create a new layout at the given sitepath. For
    example,
     
    .. code-block:: bash

        pagd -l 'pagd.myblog' create

    uses ``pagd.myblog`` plugin to create a source layout.
    """
    implements( ICommand )

    cmd = 'create'
    description = 'Create a source layout.'

    #---- ICommand API
    def subparser( self, parser, subparsers ):
        """:meth:`pluggdapps.interfaces.ICommand.subparser` interface method.

        * -g switch can be used to supply a configuration file for layout.
        * -f switch will overwrite if ``sitepath`` already contains a layout.
        """
        self.subparser = subparsers.add_parser( 
                                self.cmd, description=self.description )
        self.subparser.set_defaults( handler=self.handle )
        self.subparser.add_argument(
                '-g', '--config-path',
                dest='configfile', default='config.json',
                help='The configuration used to generate the site')
        self.subparser.add_argument(
                '-f', '--force', dest='overwrite',
                action='store_true', default=False,
                help='Overwrite the source layout if it exists')
        return parser

    def handle( self, args ):
        """:meth:`pluggdapps.interfaces.ICommand.handle` interface method.
        
        Instantiate a layout plugin and apply create() method on the
        instantiated plugin. ``sitepath`` and ``siteconfig`` references willbe
        passed as settings dictionary.
        """
        configfile = join( args.sitepath, args.configfile )
        if isfile(configfile) :
            siteconfig = json2dict( join( args.sitepath, configfile ))
            layoutname = siteconfig['layout']
        else :
            layoutname = args.layout
            siteconfig = {}

        sett = { 'sitepath' : args.sitepath,
                 'siteconfig' : siteconfig
               }
        layout = self.qp( ILayout, args.layout, settings=sett )
        if not layout :
            raise Exception(
                "The given layout is invalid. Please check if you have the "
                "`layout` in the right place and the environment variable "
                "has been setup properly if you are using custom path for "
                "layouts")
        self.pa.loginfo(
            "Creating site at [%s] with layout [%s] ..." %
            (args.sitepath, args.layout))
        layout.create( overwrite=args.overwrite )
        self.pa.loginfo("... complete")

