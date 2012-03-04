#!/usr/bin/env python
###############################################################################
## GMusicTagger Project
##
## Copyright (C) 2011 Guillermo Guerrero g.guerrero.bus@gmail.com
##
## This program is free software; you can redistribute it and/or modify
## it under the terms of the GNU General Public License as published by
## the Free Software Foundation; either version 3 of the License, or
## (at your option) any later version.
##
## This program is distributed in the hope that it will be useful,
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
## GNU General Public License for more details.
##
## You should have received a copy of the GNU General Public License
## along with this program; if not, write to the Free Software
## Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
###############################################################################

import os
import sys
from core import env
from ui.app import GMusicTagger

def check_config(config_file):
    if not os.path.exists(config_file):
        import core.preferences as pref   
        config = pref.Config(config_file)
        config.create_config()

if __name__ == "__main__":
    if not os.path.exists(env.CONFIG_PATH):
        os.makedirs(env.CONFIG_PATH)
    config_file = os.path.join(env.CONFIG_PATH,env.CONFIG_FILE)
    check_config(config_file)
          
    gmusictaggerglade = os.path.join(env.GLADE_PATH,env.GLADE_MAIN)
    gmusictagger = GMusicTagger(path=gmusictaggerglade)
    gmusictagger.run()
    
