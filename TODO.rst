* Title line should include age of the document,
  ``by prataprc - last modified: Sun Jun 02, 2013 - 2years 1month old``

* Check copyright header for all modules.

* Added social sharing for `myblog` layout.

* Add discus plugin for `myblog` layout.

* In command-line documentation article indicate that developers should check
  for existing commands before authoring a new-command to avoid duplicating
  names.

* Create a basic layout for simple web sites and make that as default in
  pagd.commands.create module and other related modules.

* `regen` option in generate sub-command is yet to be implemented.

* Cache templates while generating the target site.

Release check-list 
-----------------

* Sphinx doc quick-start, one time activity.
    sphinx-quickstart   # And follow the prompts.
    sphinx-apidoc -f -d 2 -T -o  \
                  sphinxdoc/source/ pluggdapps \
                  $(APIDOC_EXCLUDE_PATH)"

* Make sure that sphinxdoc/modules/ has all the modules that need to be
  documented.

* Change the release version in 
    ./CHANGELOG,
    ./pagd/__init__.py

* Update setup.py and MANIFEST.in for release

* Enter virtual environment and upload the source into pypi.
        make upload

* Upload documentation zip.

* After making the release, taging the branch, increment the version number.

* Create a tag and push the tagged branch to 
    github.com

