# -*- coding: utf-8 -*-

# This file is subject to the terms and conditions defined in
# file 'LICENSE', which is part of this source code package.
#       Copyright (c) 2013 R Pratap Chakravarthy

from   os       import listdir
from   os.path  import join, splitext, isfile, isdir, relpath, abspath, \
                       dirname, split, getmtime
from   copy     import deepcopy
import os, time

from   pluggdapps.plugin    import Plugin, implements
import pluggdapps.utils     as h
from   pagd.interfaces      import ILayout, IContent, ITemplate, IXContext
from   pagd.lib             import json2dict, pagd, findtemplate, Site, Page

class MyBlog( Plugin ):
    """Layout plugin to generate personal blog sites."""
    implements(ILayout)
    layoutpath = join( dirname(__file__), 'myblog')

    _templates = {
        'ttl' : 'pagd.Tayra',
        'jinja2' : 'pagd.Jinja2',
        'j2' : 'pagd.Jinja2',
        'mako' : 'pagd.Mako',
    }
    _xcontexts = {}
    _icontents = {}

    def __init__( self ):
        self.sitepath = self['sitepath']
        self.siteconfig = json2dict( join( self.sitepath, self['configfile']))
        self._templates = {
            typ : self.qp( ITemplate, caname, self.siteconfig )
            for typ, caname in self._templates.items() }
        
        self._xcontexts = { p.caname : p for p in self.qps(IXContext) }
        self._icontents = { p.caname : p for p in self.qps(IContent) }

    #---- ILayout interface methods

    def is_exist(self):
        xs = [ 'configfile', 'contentdir', 'templatedir' ]
        x, y, z = [join(self.sitepath, self[x]) for x in xs]
        return isfile(x) and isdir(y) and isdir(z)

    def create(self, **kwargs) :
        if not isdir( self['sitepath'] ) :
            os.makedirs( self['sitepath'], exist_ok=True )
        _vars = { 'sitepath' : self.sitepath,
                }
        h.template_to_source( self.layoutpath, self.sitepath, _vars )

    def generate(self, buildtarget, **kwargs) :
        regen = kwargs['regen']
        for page in self.pages() :
            path = join(buildtarget, page.relpath)
            fname = abspath( join( path, page.pagename+'.html' ))
            self.pa.loginfo("    Generating `%r`" % fname)
            html = self.pagegenerate( page )
            os.makedirs( path, exist_ok=True )
            open(fname, 'w').write(html)

    SPECIALPAGES = ['_context.json']
    def pages(self):
        contentdir = join( self.sitepath, *self['contentdir'].split('/') )
        site = Site()
        site.sitepath = self.sitepath
        site.siteconfig = self.siteconfig
        for dirpath, dirs, files in os.walk(contentdir):
            files = sorted(files)
            [ files.remove(f) for f in self.SPECIALPAGES if f in files ]
            while files :
                pagename, contentfiles, context, files = \
                        pagd( join(contentdir, dirpath), files )
                page = Page()
                page.site = site
                page.pagename = pagename
                page.relpath = relpath(dirpath, contentdir)
                page.urlpath = join( relpath(dirpath, contentdir), pagename)
                page.urlpath = '/'.join( page.urlpath.split( os.sep ))
                page.contentfiles = contentfiles

                page.context = { 'site' : page.site, 'page' : page }
                page = self.pagecontext( page )
                page.context.update( context )

                page = self.pagecontent( page )
                # page content can also have context, in the form of metadata
                for fpath, metadata, content in page.articles :
                    page.context.update( metadata )

                # Fix some context.
                if 'title' not in page.context :
                    page.context['title'] = page.pagename
                yield page

    def pagecontext( self, page ):
        contentdir = join( self.sitepath, *self['contentdir'].split('/') )
        contexts = self.default_context(contentdir, page)

        # From the list of context dictionaries in `contexts` check for
        # `_xcontext` attribute and fetch the context from external source.
        for c in contexts :
            page.context.update(c)
            plugin = self._xcontexts.get( c.get('_xcontext', None), None )
            page.context.update( plugin.fetch(page) ) if plugin else None

        tms = max([ getmtime(f) for f in page.contentfiles ])
        page.context.update({
            'last_modified' :time.strftime( "%a %b %d, %Y", time.gmtime(tms) ),
        })
        return page

    def pagecontent( self, page ):
        name = page.context.get('IContent', self['IContent'])
        icont = self._icontents.get( name, _default_settings['IContent'] )
        page.articles = icont.articles(page)
        return page

    def pagegenerate( self, page ):
        page.templatefile = self.pagetemplate(page)
        _, ext = splitext(page.templatefile)
        ttype = page.context.get('templatetype', ext.lstrip('.'))
        return self._templates[ttype].render( page )

    def pagetemplate( self, page ):
        tmplpath = join( self.sitepath, *self['templatedir'].split('/') )
        tmplfile = None
        dr = abspath( join( tmplpath, page.relpath ))
        if 'template' in page.context :
            tmplfile = asset_spec_to_abspath( page.context['template'] )
            tmplfile = tmplfile if tmplfile and isfile(tmplfile) else None
        if tmplfile == None and isdir(dr) :
            tmplfile = findtemplate(dr, pagename=page.pagename)
            tmplfile = tmplfile if tmplfile and isfile(tmplfile) else None
        if tmplfile == None :
            path = page.relpath
            while tmplfile == None and path :
                d = join( tmplpath, path )
                if isdir(d) :
                    tmplfile = findtemplate(d, default=self['default_template'])
                    tmplfile = tmplfile \
                                    if tmplfile and isfile(tmplfile) else None
                path, _ = split( path )
        return tmplfile

    #---- Local functions
    def default_context( self, contentdir, page ):
        """Return a list of context dictionaries from default-context under each
        sub-directory of content-page's path."""
        path = page.relpath.strip(os.sep)
        contexts = []
        fname = self['default_context']
        while path :
            f = join(contentdir, path, fname)
            contexts.insert(0, json2dict(f)) if isfile(f) else None
            path, _ = split( path )
        return contexts


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
        return settings


_default_settings = h.ConfigDict()
_default_settings.__doc__ = MyBlog.__doc__

_default_settings['sitepath'] = {
    'default' : '',
    'types'   : (str,),
    'help'    : "Target directory to place layout files. If not specified "
                "uses the current working directory."
}
_default_settings['configfile'] = {
    'default' : 'config.json',
    'types'   : (str,),
    'help'    : "Configuration file name under sitepath, will be interpreted "
                "as site-configuration. Refer to corresponding layout "
                "documentation for information on available configuration "
                "settings."
}
_default_settings['contentdir'] = {
    'default' : '_contents',
    'types'   : (str,),
    'help'    : "Sub-direcory name under sitepath that contains all page "
                "contents for the site."
}
_default_settings['templatedir'] = {
    'default' : '_templates',
    'types'   : (str,),
    'help'    : "Sub-direcory name under sitepath that contains all page "
                "templates. Page templates are used to generate the final "
                "site-html files."
}
_default_settings['default_context'] = {
    'default' : '_context.json',
    'types'   : (str,),
    'help'    : "Context file name to look for in content sub-directories as "
                "default context."
}
_default_settings['IContent'] = {
    'default' : 'pagd.native',
    'types'   : (str,),
    'help'    : "Plugin to generate html content from page-content files."
}
_default_settings['default_template'] = {
    'default' : '_default',
    'types'   : (str,),
    'help'    : "Base name of a template file expected under a sub-directory "
                "of layout's template directory."
}

