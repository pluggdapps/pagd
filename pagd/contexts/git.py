# -*- coding: utf-8 -*-

# This file is subject to the terms and conditions defined in
# file 'LICENSE', which is part of this source code package.
#       Copyright (c) 2013 R Pratap Chakravarthy

from   os.path      import join
import subprocess

from   pluggdapps.plugin        import Plugin, implements
import pluggdapps.utils         as h
import pluggdapps.interfaces

import pagd.interfaces

class Git( Plugin ):
    """Plugin to fetch page's context from git, if available, and compose them
    into a dictionary of page's metadata."""

    implements( pagd.interfaces.IXContext )

    cmd = ["git", "log", '--pretty="%cn ; %ce ; %ct']
    def fetch( self, page ):
        """Provides the following context from git repository log for the
        file,

        .. code-block:: python

            { 'author' : <string>,
              'email' : <string>,
              'createdon' : <date-string>,
              'last_modified' : <date-string>
            }

        - `author` will be original author who created the file.
        - `email` will be email-id of the original author,
        - `date-string` will be of the format 'Mon Jun 10, 2013' and will
          refer to author's local-time.
        """
        for fpath in page.contentfiles :
            try :
                logs = subprocess.check_output(self.cmd+[fpath]).splitlines()
                _, _, last_modified = logs[0].decode('utf-8').split(" ; ")
                author, email, createdon = logs[-1].decode('utf-8').split(" ; ")
            except :
                raise
                author, email, createdon, last_modified = '', '', '', ''

        return { 'author' : author.strip(' "\''),
                 'email' : email.strip(' "\''),
                 'createdon' : h.age( int(createdon.strip()) ),
                 'last_modified' : h.age( int(last_modified.strip()) ) }
