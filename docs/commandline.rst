Command line script
===================

While installing the package using pip, a command line script ``pagd``
is automatically created in **bin/** directory. If you are installing it
inside a virtual environment you can expect it in the directory
**<virtual-env-path>/bin/** directory. 

Once the command is available in your environment or via ``PYTHONPATH``,


.. code-block:: text
    :linenos:

    $ pagd --help
    usage: pagd [-h] [-s SITEPATH] [-c CONFIG] [-l LAYOUT]

    `pagd` command line script.

    optional arguments:
      -h, --help            show this help message and exit
      -s SITEPATH, --sitepath SITEPATH
                            Location of site's layout source.
      -c CONFIG             Specify config file.
      -l LAYOUT, --layout LAYOUT
                            Layout-type for the new site


Few command line use cases,

.. code-block:: bash
    :linenos:

    # Create a new source layout using `pagd.myblog` plugin under sitepath
    # `/home/me/mysite`.
    $ pagd -l pagd.myblog -s /home/me/mysite create

    # generate the static web-site under `docroot/` relative to sitepath 
    # `/home/me/mysite`, i.e, `/home/me/mysite/docroot`
    $ pagd -s /home/me/mysite gen -t ./docroot
