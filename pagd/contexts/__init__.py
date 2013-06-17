# -*- coding: utf-8 -*-

# This file is subject to the terms and conditions defined in
# file 'LICENSE', which is part of this source code package.
#       Copyright (c) 2013 R Pratap Chakravarthy

"""Contains a collection of plugins to fetch page context from external
sources like repository, database etc ..."""

import pagd.contexts.git    # Fetch page's x-context from git repository.
import pagd.contexts.hg     # Fetch page's x-context from hg repository.
