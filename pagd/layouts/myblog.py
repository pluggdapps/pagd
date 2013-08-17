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
    """A layout plugin to generate personal blog sites. Support create, gen,
    newpage interfaces APIs for corresponding sub-commands.
    """

    implements(ILayout)
    layoutpath = join( dirname(__file__), 'myblog')

    def __init__( self ):
        self.sitepath = self['sitepath']
        if isinstance(self['siteconfig'], dict) :
            self.siteconfig = self['siteconfig']
        else :
            self.siteconfig = json2dict( join( self['siteconfig'] ))
        self.plugins = self._plugins( self.sitepath, self.siteconfig )

    #---- ILayout interface methods

    def is_exist(self):
        """:meth:`padg.interfaces.ILayout.is_exist` interface method."""

        xs = [ 'configfile', 'contentdir', 'templatedir' ]
        x, y, z = [join(self.sitepath, self[x]) for x in xs]
        return isfile(x) and isdir(y) and isdir(z)

    def create(self, **kwargs) :
        """Creates a new layout under ``sitepath``. Uses the directory tree
        under `pagd:layouts/myblog` as a template for the new layout. Accepts
        the following variable while creating,

        ``sitepath``,
            directory-path under which the new layout had to be created.
        """
        if not isdir( self['sitepath'] ) :
            os.makedirs( self['sitepath'], exist_ok=True )
        _vars = { 'sitepath' : self.sitepath, }
        overwrite = kwargs.get('overwrite', False)
        h.template_to_source( self.layoutpath, self.sitepath, _vars,
                              overwrite=overwrite, verbose=True )

    def generate(self, buildtarget, **kwargs) :
        """Generate a static, personal blog site from the layout under
        ``sitepath``. Note that previously a new-layout must have been created
        using this plugin and available under `sitepath`.
        
        This method,

        - iterates over each page availabe under the source-layout,
        - gathers page contexts.
        - translates page content into html.
        - locate a template for the page and generate the html for page.

        Refer to :meth:`pages` method to know how pages are located under
        layout's content-directory.
        """
        regen = kwargs.get('regen', True)
        srcfile = kwargs.get('srcfile', None)
        for page in self.pages() :
            path = abspath( join( buildtarget, page.relpath ))
            fname = page.pagename + '.html'
            self.pa.loginfo("    Generating `%r`" % join(page.relpath, fname) )

            # Gather page context
            page.context.update( self.pagecontext( page ))

            # Gather page content
            page.articles = self.pagecontent( page )

            # page content can also have context, in the form of metadata
            # IMPORTANT : myblog will always have one article only.
            for fpath, metadata, content in page.articles :
                page.context.update( metadata )
                page.context.update(
                    self._fetch_xc( metadata.get('_xcontext', ''), page ))

            # If skip_context is present then apply them,
            page = self._skip_context( page )

            # Find a template for this page.
            page.templatefile = self.pagetemplate(page) # Locate the templage
            if isinstance(page.templatefile, str) :
                _, ext = splitext(page.templatefile)
                ttype = page.context.get('templatetype', ext.lstrip('.'))
                # generate page's html
                html = self._tmpl2plugin( self.plugins, ttype ).render( page )
                os.makedirs(path, exist_ok=True) if not isdir(path) else None
                open( abspath( join( path, fname )), 'w' ).write(html)


    SPECIALPAGES = ['_context.json']
    def pages(self):
        """Individual pages are picked based on the relative directory path
        along with filenames. Note that file extensions are not used to
        differentite pages, they are only used to detect the file type and
        apply corresponding translation algorithm to get page's html.
        """
        contentdir = join( self.sitepath, *self['contentdir'].split('/') )
        site = Site()
        site.sitepath = self.sitepath
        site.siteconfig = self.siteconfig
        for dirpath, dirs, files in os.walk(contentdir):
            files = sorted(files)
            [ files.remove(f) for f in self.SPECIALPAGES if f in files ]
            while files :
                pagename, contentfiles, files = \
                        pagd( join(contentdir, dirpath), files )
                page = Page()
                page.site = site
                page.pagename = pagename
                page.relpath = relpath(dirpath, contentdir)
                page.urlpath = join( relpath(dirpath, contentdir), pagename)
                page.urlpath = '/'.join( page.urlpath.split( os.sep ))
                page.contentfiles = contentfiles
                page.context = self.config2context( self.siteconfig )
                page.context.update({
                    'site'    : page.site,
                    'page'    : page,
                    'title'   : page.pagename,
                    'summary' : '',
                    'layout'  : self.caname,
                    'author'  : None,
                    'email'   : None,
                    'createdon'     : None,
                    'last_modified' : None,
                    'date'  : None,
                })
                page.articles = []
                yield page

    def pagecontext( self, page ):
        """Gathers default context for page.

        Default context is specified by one or more JSON files by name
        `_context.json` that is located under every sub-directory that
        leads to the page-content under layout's content-directory.
        `_context.json` found one level deeper under content directory will
        override `_context.json` found in the upper levels.

        Also, if a pagename has a corresponding JSON file, for eg,
        ``<layout>/_contents/path/hello-world.rst`` file has a corresponding
        ``<layout>/_contents/path/hello-world.json``, it will be interepreted
        as the page's context. This context will override all the default
        context.

        If `_xcontext` attribute is found in a default context file, it
        will be interpreted as plugin name implementing :class:`IXContext`
        interface. The plugin will be queried, instantiated, to fetch context
        information from external sources like database.

        Finally ``last_modified`` time will be gathered from content-file's
        mtime statistics.
        """
        contentdir = join( self.sitepath, *self['contentdir'].split('/') )
        contexts = self.default_context(contentdir, page)

        # Page's context, if available.
        page_context_file = join(page.relpath, page.pagename) + '.json'
        c = json2dict(page_context_file) if isfile(page_context_file) else None
        contexts.append(c) if c else None

        context = {}
        # From the list of context dictionaries in `contexts` check for
        # `_xcontext` attribute and fetch the context from external source.
        for c in contexts :
            context.update(c)
            context.update( self._fetch_xc( c.get('_xcontext', ''), page ))
        return context

    def pagecontent( self, page ):
        """Pages are located based on filename, and the file extension is not
        used to differential pages. Hence there can be more than one file by
        same filename, like, ``_contents/hello-world.rst``,
        ``_contents/hello-world.md``. In such cases, all files will be
        considered as part of same page and translated to html based on the
        extension type.

        Return a single element list of articles, each article as tuple.
        Refer to :class:``Page`` class and its ``articles`` attribute to know
        its data-structure."""

        n = page.context.get('IContent', self['IContent'])
        name = n if n in self.plugins else _default_settings['IContent']
        icont = self.plugins.get( name, None )
        articles = icont.articles(page) if icont else []
        return articles

    def pagetemplate( self, page ):
        """For every page that :meth:`pages` method iterates, a corresponding
        template file should be located. It is located by following steps.

        - if page's context contain a ``template`` attribute, then its value
          is interpreted as the template file for page in asset specification
          format.
        - join the relative path of the page with ``_template`` sub-directory
          under the layout, and check whether a template file by pagename is
          available. For eg, if pagename is ``hello-world`` and its relative
          path is ``blog/2010``, then a template file
          ``_templates/blog/2010/hello-world`` will be lookup. Note that the
          extensio of the template file is immaterial.
        - If both above steps have failed then will lookup for a ``_default``
          template under each sub-directory leading to
          ``_templates/blog/2010/``.
        """
        tmplpath = join( self.sitepath, *self['templatedir'].split('/') )
        tmplfile = None
        dr = abspath( join( tmplpath, page.relpath ))
        if page.context.get('template', None) == False :
            tmplfile = False
        if tmplfile == None and 'template' in page.context :
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


    def newpage(self, pagename):
        contentdir = join( self.sitepath, *self['contentdir'].split('/') )
        try     : _, ext = splitext(pagename)
        except  : ext = '.rst'
        filepath = join( self.sitepath, contentdir, pagename+'.rst' )
        os.makedirs( dirname(filepath), exist_ok=True )
        open(filepath, 'w').write()
        self.pa.loginfo("New page create - %r", filepath)


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

    def config2context( self, siteconfig ):
        xd = { x : siteconfig[x] 
               for x in [ 'disqus', 'show_email', 'social_sharing', 'copyright',
                          'google_webfonts', 'style', 'age_scale', ]
             }
        return xd

    def _plugins( self, sitepath, siteconfig ):
        """Instantiate plugins available for :class:`ITemplate`,
        :class:`IXContext` and :class:`IContent` interfaces.
        
        siteconfig and sitepath will be passed as plugin-settings for all
        instantiated plugins. 
        """
        sett = { 'sitepath'   : sitepath, 'siteconfig' : siteconfig }
        plugins = self.qps( ITemplate, settings=sett ) + \
                  self.qps( IXContext, settings=sett ) + \
                  self.qps( IContent, settings=sett )
        return { p.caname : p for p in plugins }

    def _tmpl2plugin( self, plugins, tmpl ):
        """For file type ``tmpl`` return the template plugin."""
        for p in plugins.values() :
            if tmpl in getattr(p, 'extensions', []) : return p
        else :
            return None

    def _skip_context(self, page):
        attrs = h.parsecsv( page.site.siteconfig.get( 'skip_context', '' )) + \
                h.parsecsv( page.context.get( 'skip_context', '' ))
        [ page.context.update(attr=None) for attr in attrs ]
        return page

    def _fetch_xc(self, _xc, page) :
        ps = h.parsecsv( _xc )
        context = {}
        for s in ps :
            p = self.plugins.get(s, None)
            context.update( p.fetch(page) ) if p else None
        return context

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

