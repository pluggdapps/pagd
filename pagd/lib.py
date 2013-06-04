# -*- coding: utf-8 -*-

# This file is subject to the terms and conditions defined in
# file 'LICENSE', which is part of this source code package.
#       Copyright (c) 2013 R Pratap Chakravarthy

"""A collection of library routines."""

from   os.path  import split, join, isfile, splitext, abspath
import os, json

__all__ = [ 'json_encode', 'json_decode' ]

def json_encode( value, encoding=None ):
    """JSON-encodes the given Python object. If `encoding` is supplied, then
    the resulting json encoded string will be converted to bytes and return
    the same, otherwise, json encodied string is returned as is."""
    # JSON permits but does not require forward slashes to be escaped.
    # This is useful when json data is emitted in a <script> tag
    # in HTML, as it prevents </script> tags from prematurely terminating
    # the javscript.  Some json libraries do this escaping by default,
    # although python's standard library does not, so we do it here.
    # http://stackoverflow.com/questions/1580647/json-why-are-forward-slashes-escaped
    s = json.dumps( value ).replace( "</", "<\\/" )
    r = s.encode( encoding ) if encoding else s
    return r

def json_decode( value, encoding=None ):
    """Convert json encoded value to Python object. If `encoding` is not
    supplied `value` is assumed to be in string, otherwise, value is expected
    in bytes and converted to string.

    Return the python object."""
    return json.loads( value.decode(encoding) if encoding else value )


def json2dict( jsonfile ):
    """Convert ``jsonfile`` to python dictionary. Return ``None`` if jsonfile
    is not found."""
    if isfile( jsonfile ) :
        txt = open(jsonfile).read()
        d = json_decode(txt) if txt else {}
    else :
        return {}
    if not isinstance( d, dict ) :
        raise Exception( "Expected %r as property of settings" % jsonfile )
    return d


def pagd(path, files) :
    """This function implements the key concept in pagd, that is, to aggregate
    content and context for target web-page.
    
    ``path``,
        Absolute directory path pointing a sub-directory under layout's
        content directory.
    ``files``,
        List of files under a sub-directory from layout's content directory.

    Return a tuple of, (pagename, page-contents, context, remaining-files)

    ``pagename``,
        name of the web-page that will appear in url-path as last path segment.
    ``page-contents``,
        List of files that can be translated to html content for page
        `pagename`.
    ``context``,
        Python dictionary of context attributes associated with page
        `pagename`.
    ``remaining-files``,
        List of files that remain after gathering contents and context for
        page `pagename`.
    """
    pagename, ext = splitext( files[0] )
    contentfiles, jsonfile = [], None
    while files :
        x, y = splitext( files[0] )
        if x == pagename and y == '.json' :
            jsonfile = files[0]
        elif x == pagename :
            contentfiles.append( join(path, files[0] ))
        else :
            break
        files.pop(0)
    context = json2dict( join( path, jsonfile )) if jsonfile else {}
    return pagename, contentfiles, context, files


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
        Dictionary of article name and its content value.

    ``context``,
        Dictionary of context attributes for page.

    ``templatefile``,
        Template file name with absolute path-name to be used for translating
        this content-page to html page.

    All the above attributes are unique for each page.
    """

def parse_metadata( text ):
    pass
