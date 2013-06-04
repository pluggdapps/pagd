#! /usr/bin/env python3.2

# -*- coding: utf-8 -*-

# This file is subject to the terms and conditions defined in
# file 'LICENSE', which is part of this source code package.
#       Copyright (c) 2013 R Pratap Chakravarthy

"""Command line script. Almost all functions of command line script are
implemented as sub-commands. To get a quick summary of available sub-commads,

.. code-block:: bash
    :linenos:

    $ pagd commands

To learn more about available subcommand refer to :mod:`pagd.commands`
package. Since sub commands are implemented as plugins, there can be other
sub-commands implemented by different package. Refer to corresponding package
for their documentation.

You can also use `--help` on the sub-command for supported options.

.. code-block:: bash
    :linenos:

    $ pagd --help
"""

import sys
from   argparse     import ArgumentParser
from   os.path      import abspath

import pluggdapps
from   pluggdapps.platform   import Pluggdapps
from   pluggdapps.interfaces import ICommand
from   pluggdapps.plugin     import PluginMeta

import pagd

def mainoptions():
    # setup main script arguments
    description = "`pagd` command line script."
    mainparser = ArgumentParser( description=description )
    mainparser.add_argument( '-s', '--sitepath',
                             dest='sitepath', default='.',
                             help="Location of site's layout source." )
    mainparser.add_argument( '-c', dest='config', 
                             default=None,
                             help="Specify config file." )
    mainparser.add_argument( '-l', '--layout',
                             dest='layout', default='pagd.myblog',
                             help='Layout-type for the new site' )
    return mainparser

def main():
    from pluggdapps import loadpackages
    import pluggdapps.commands

    loadpackages()  # This is important, otherwise plugins in other packages 
                    # will not be detected.

    # Create command line parser.
    # Get a list of sub-commands supported in command line.
    # Take only the command-line parameters uptil a subcommand.
    mainparser = mainoptions()
    mainargs = pluggdapps.commands.mainargs(ICommand, 'pagd.*', sys.argv[1:])
    args = mainparser.parse_args( mainargs )

    pa = Pluggdapps.boot( args.config )
    subcommands = pa.qpr( pa, ICommand, 'pagd.*' )

    # setup sub-command arguments
    subparsers = mainparser.add_subparsers( help="Sub-commands" )
    [ subcmd.subparser( mainparser, subparsers ) for subcmd in subcommands ]

    # Do a full parsing of command line arguments.
    args = mainparser.parse_args()

    args.sitepath = abspath( args.sitepath )

    # Corresponding handler is expected to be registered during subparser()
    # call above.
    args.handler( args )

if __name__ == '__main__' :
    main()
