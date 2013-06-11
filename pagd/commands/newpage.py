# -*- coding: utf-8 -*-

# This file is subject to the terms and conditions defined in
# file 'LICENSE', which is part of this source code package.
#       Copyright (c) 2013 R Pratap Chakravarthy

from   os.path               import join, isfile, abspath
from   pluggdapps.plugin     import Singleton, implements
from   pluggdapps.interfaces import ICommand

from   pagd.interfaces       import ILayout
from   pagd.lib              import json2dict

class NewPage( Singleton ):
    """Sub-command plugin to generate a new content page under
    layout-sitepath.
    """
    implements( ICommand )

    cmd = 'newpage'
    description = 'Create a new content page.'

    #---- ICommand API
    def subparser( self, parser, subparsers ):
        """:meth:`pluggdapps.interfaces.ICommand.subparser` interface method.
        """
        self.subparser = subparsers.add_parser( 
                                self.cmd, description=self.description )
        self.subparser.set_defaults( handler=self.handle )
        self.subparser.add_argument(
                '-g', '--config-path',
                dest='configfile', default='config.json',
                help='The configuration used to generate the site')
        self.subparser.add_argument(
                'pagename', nargs=1,
                help='File name, extension not provided defaults to rst' )
        return parser

    def handle( self, args ):
        """:meth:`pluggdapps.interfaces.ICommand.handle` interface method.
        
        Instantiate a layout plugin and apply newpage() method on the
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
        layout = self.qp( ILayout, layoutname, settings=sett )
        layout.newpage( pagename )

