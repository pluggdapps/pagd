# -*- coding: utf-8 -*-

# This file is subject to the terms and conditions defined in
# file 'LICENSE', which is part of this source code package.
#       Copyright (c) 2013 R Pratap Chakravarthy

def make_site(sitepath, config, deploy=None):
    """Creates a site object from the given sitepath and the config file."""
    config = Config(sitepath, config_file=config)
    if deploy:
        config.deploy_root = deploy
    return Site(sitepath, config)


import pagd.commands.commands
import pagd.commands.create
import pagd.commands.generate
import pagd.commands.newpage
import pagd.commands.publish
