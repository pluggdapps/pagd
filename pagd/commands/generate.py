# -*- coding: utf-8 -*-

# This file is subject to the terms and conditions defined in
# file 'LICENSE', which is part of this source code package.
#       Copyright (c) 2013 R Pratap Chakravarthy

from   os.path               import join, isfile, abspath
from   pluggdapps.plugin     import Singleton, implements
from   pluggdapps.interfaces import ICommand

from   pagd.interfaces       import ILayout
from   pagd.lib              import json2dict

class Gen( Singleton ):
    """Sub-command plugin to generate static web site at the given target
    directory. If a target directory is not specified, it uses layout's
    default target directory. For more information refer to corresponding
    layout plugin's documentation.
    """
    implements( ICommand )

    cmd = 'gen'
    description = 'Generate a static site for the give layout and content'

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
                '-t', '--build-target', dest='buildtarget',
                default='.',
                help="Location of target site that contains generated html.")
        self.subparser.add_argument(
                '-r', '--regen', dest='regen',
                action='store_true', default=False,
                help='Regenerate all site pages.')
        return parser

    def handle( self, args ):
        """:meth:`pluggdapps.interfaces.ICommand.handle` interface method.

        Instantiate a layout plugin and apply generate() method on the
        instantiated plugin. ``sitepath`` and ``siteconfig`` references willbe
        passed as settings dictionary.
        """
        siteconfig = join( args.sitepath, args.configfile )
        siteconfig = json2dict( siteconfig )
        layoutname = siteconfig.get( 'layout', args.layout )
        sett = { 'sitepath'   : args.sitepath,
                 'siteconfig' : siteconfig
               }
        layout = self.qp( ILayout, layoutname, settings=sett )
        self.pa.loginfo(
            "Generating site at [%s] with layout [%s] ..." %
            (args.sitepath, layoutname))
        layout.generate( abspath(args.buildtarget), regen=args.regen )
        self.pa.loginfo("... complete")
