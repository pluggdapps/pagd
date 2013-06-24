A roadmap of things to do
=========================

* Merge siteconfig with page-context. At the end of it, even configuration
  information is part of context and this gives a unified picture to template
  developers, while for the users they get to enjoy the notion of
  site-configuration and context-manipuation.

* age()-scale is calculated statically, so it does not make sense if the site
  is goint to be generated once in a while. On the other hand if the site is
  going to be generated periodically, then corresponding scale-factor can be
  choosen by user. So make ''git.*'' plugin configuration available for
  IXContext plugins ?

* A per-page/default context option to skip metadata from page, even if it is
  available.

* if more that one article-content is detected for the same page-url, how to
  generate the HTML ? as list of individual articles ? or as tabbed version of
  articles ?

* `regen` option in generate sub-command is yet to be implemented.

* Cache templates while generating the target site.

* Merge support when using `create -f`. A 3-way merge is there, find a clean
  solution for this.

* for `pagd.myblog` layout,

  * Support asciidoc content parsing.
  * Facebook integration. There are aweful lot of ways to integrate a page with
    facebook. Do we really need them all ?


Release check-list 
------------------

- Sphinx doc quick-start, one time activity.
    sphinx-quickstart   # And follow the prompts.
    sphinx-apidoc -f -d 2 -T -o  docs/ pagd $(APIDOC_EXCLUDE_PATH)"

- Change the release version in ./CHANGELOG, ./pagd/__init__.py

- Update TODO.rst if any, because both CHANGELOG.rst and TODO.rst are referred
  by README.rst.

- copy ~/oss/magnific-popup-git/dist/
  {magnific-popup.css,jquery.magnific-popup.min.js
  files to pagd/layouts/myblog/media/magnific-popup/ directory.

- Check whether release changelogs in CHANGELOG.rst have their release-timeline
  logged, atleast uptill the previous release.

- Update setup.py and MANIFEST.in for release

- Make sure that sphinxdoc/modules/ has all the modules that need to be
  documented.

- Enter virtual environment and upload the source into pypi.
        make upload

- Upload documentation zip.

- After making the release, taging the branch, increment the version number.

- Create a tag and push the tagged branch to 
    github.com

