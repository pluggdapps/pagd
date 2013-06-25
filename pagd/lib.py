# -*- coding: utf-8 -*-

# This file is subject to the terms and conditions defined in
# file 'LICENSE', which is part of this source code package.
#       Copyright (c) 2013 R Pratap Chakravarthy

"""A collection of library routines."""

from   os.path  import split, join, isfile, splitext, abspath
import os, json, time

import pluggdapps.utils as h

def json2dict( jsonfile ):
    """Convert ``jsonfile`` to python dictionary. Return ``None`` if jsonfile
    is not found."""
    if isfile( jsonfile ) :
        txt = open(jsonfile).read()
        d = h.json_decode(txt) if txt else {}
    else :
        return {}
    if not isinstance( d, dict ) :
        raise Exception( "Expected %r as property of settings" % jsonfile )
    return d


def pagd(path, files) :
    """This function implements the key concept in pagd, that is, to aggregate
    content and for target web-page.
    
    ``path``,
        Absolute directory path pointing a sub-directory under layout's
        content directory.
    ``files``,
        List of files under a sub-directory from layout's content directory.

    Return a tuple of, (pagename, page-contents, remaining-files)

    ``pagename``,
        name of the web-page that will appear in url-path as last path segment.
    ``page-contents``,
        List of files that can be translated to html content for page
        `pagename`.
    ``remaining-files``,
        List of files that remain after gathering contents.
    """
    pagename, ext = splitext( files[0] )
    contentfiles = []
    while files :
        x, y = splitext( files[0] )
        if x == pagename :
            contentfiles.append( join(path, files[0] ))
        else :
            break
        files.pop(0)
    return pagename, contentfiles, files


def findtemplate( subdir, pagename=None, default=None ):
    """Find a matching template under ``subdir``.

    ``subdir``,
        Directory path that shall contain one or more template files.
    ``pagename``,
        Page-name for which this function shall find a corresponding
        template-file.
    ``default``,
        Basename of default-template.
    """
    if pagename :
        expected_file = pagename
    elif default :
        expected_file = default

    for f in os.listdir(subdir) :
        if f.startswith(expected_file) :
            tmplfile = abspath( join( subdir, f ))
            break
    else :
        tmplfile = None
    return tmplfile


agescales = [("year", 3600 * 24 * 365),
             ("month", 3600 * 24 * 30),
             ("week", 3600 * 24 * 7),
             ("day", 3600 * 24),
             ("hour", 3600),
             ("minute", 60),
             ("second", 1)]
def age( then, format="%a %b %d, %Y", scale="year" ):
    """convert (timestamp, tzoff) tuple into an age string. both `timestamp` and
    `tzoff` are expected to be integers."""

    plural = lambda t, c : t if c == 1 else (t + "s")
    fmt = lambda t, c : "%d %s" % (c, plural(t, c))

    now = time.time()
    if then > now :
        return 'in the future'

    threshold = h.dropwhile( lambda x : x[0] != scale, agescales )[0][1]
    delta = max(1, int(now - then))
    if delta > threshold :
        return time.strftime(format, time.gmtime(then))

    for t, s in agescales:
        n = delta // s
        if n >= 2 or s == 1:
            return '%s ago' % fmt(t, n)

class Site(object):
    """Abstraction object to hold following attributes.

    ``sitepath``,
        Absolute path to where the source files for the site is present.

    ``siteconfig``,
        A python dictionary of configuration settings application to entire
        site.

    All the above attributes have site-wide scope.
    """
        
class Page(object):
    """Abstraction object to hold following attributes.

    ``site``,
        an instance of :class:`Site` class that contains this page.

    ``pagename``,
        name of the page that will appear in url-path as last path segment.

    ``relpath``,
        relative path from `sitepath`, where pagename is located.

    ``urlpath``,
        url path relative to script-path. Includes `pagename` as the last
        segment in the path.

    ``contentfiles``,
        List of files, in absolute path, that contains contents for this page.

    ``articles``,
        List of article tuples which each tuple is made up of,
        ``( article's fpath, article-context, html-text )``. Article's
        file-path is the absolute path of the content file which was
        translated to `html-text`. Article's context  is ``page.context``
        overrided with meta-data from file-content.

    ``context``,
        Dictionary of context attributes for page.

    ``templatefile``,
        Template file name with absolute path-name to be used for translating
        this content-page to html page.

    All the above attributes are unique for each page.
    """

