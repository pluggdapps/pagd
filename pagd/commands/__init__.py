# -*- coding: utf-8 -*-

# This file is subject to the terms and conditions defined in
# file 'LICENSE', which is part of this source code package.
#       Copyright (c) 2013 R Pratap Chakravarthy

"""This package contain a collection of sub-command plugins for `pagd` script.
Sub-commands should implement :class:`pluggdapps.interfaces.ICommand`
interface.

TODO: we should define a separate sub-command interface for pagd

How to implement a sub-command plugin
-------------------------------------

Just like any other plugin, derive your class from `Plugin` base class and
declare that the class implements :class:`pluggdapps.interfaces.ICommand`
interface. Refer to `ICommand` interface class to learn more about sub-command
callbacks. And check out existing sub-command plugins as well.

Note that sub-command plugins normally invoke :class:`ILayout` methods. And
form there it is upto the layout-plugin to get the job done.
"""

import pagd.commands.commands
import pagd.commands.create
import pagd.commands.generate
import pagd.commands.newpage
import pagd.commands.publish


