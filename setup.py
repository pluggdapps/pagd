# -*- coding: utf-8 -*-

# This file is subject to the terms and conditions defined in
# file 'LICENSE', which is part of this source code package.
#       Copyright (c) 2013 R Pratap Chakravarthy

import re
from   setuptools import setup, find_packages
from   os.path    import abspath, dirname, join

here = abspath( dirname(__file__) )
try :
    LONG_DESCRIPTION = open( join( here, 'README.rst' )).read(
                           ).replace(':class:`', '`'
                                    ).replace(':mod:`', '`'
                                             ).replace(':meth:`', '`')
except :
    LONG_DESCRIPTION = ''

version = re.compile( 
            r".*__version__[ ]*=[ ]*'(.*?)'",
            re.S 
          ).match( 
            open( join( here, 'pagd', '__init__.py' )).read()).group(1)

description='An integrated web templating environment'

classifiers = [
'Development Status :: 4 - Beta',
'Environment :: Web Environment',
'Intended Audience :: Developers',
'Programming Language :: Python :: 3.2',
'Topic :: Internet :: WWW/HTTP',
]

setup(
    name='pagd',
    version=version,
    py_modules=[],
    package_dir={},
    packages=find_packages(),
    ext_modules=[],
    scripts=[],
    data_files=[],
    package_data={},                        # setuptools / distutils
    include_package_data=True,              # setuptools
    exclude_package_data={},                # setuptools
    zip_safe=False,                         # setuptools
    entry_points={                          # setuptools
        'console_scripts' : [
           'pagd = pagd.script:main',
        ],
        'pluggdapps' : [
            'package=pagd:package',
        ],
    },
    install_requires=[                      # setuptools
        'tayra>=0.43dev',
    ],
    extras_require={},                      # setuptools
    setup_requires={},                      # setuptools
    dependency_links=[],                    # setuptools
    namespace_packages=[],                  # setuptools

    provides=[ 'pagd', ],
    requires='',
    obsoletes='',

    author='Pratap Chakravarthy',
    author_email='prataprc@gmail.com',
    maintainer='Pratap Chakravarthy',
    maintainer_email='prataprc@gmail.com',
    url='http://pythonhosted.org/pagd/',
    download_url='',
    license='General Public License',
    description=description,
    long_description=LONG_DESCRIPTION,
    platforms='',
    classifiers=classifiers,
    keywords=[ 'template, web, html, css, pluggdapps' ],
)
