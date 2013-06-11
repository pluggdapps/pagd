# -*- coding: utf-8 -*-

# This file is subject to the terms and conditions defined in
# file 'LICENSE', which is part of this source code package.
#       Copyright (c) 2013 R Pratap Chakravarthy

"""A collection of plugins to handle layout templates. Note that these plugins
does not stipulate how template files are to be organised. It is upto the
layout plugins to define that and subsequently pick the correct template for
each page.

The template plugin simply accepts a template file and context dictionary,
more specifically :class:`Page` instance, to generate the final html text for
the page."""

import pagd.templates.tayra
import pagd.templates.jinja2
import pagd.templates.mako
