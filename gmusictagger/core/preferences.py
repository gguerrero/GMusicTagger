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

import sys
import os
import ConfigParser
import core.env as env

class Config(ConfigParser.ConfigParser):
    def __init__(self, configfile):
        ConfigParser.ConfigParser.__init__(self)
        self.configfile = configfile
        try:
            self.readfp(open(self.configfile,'r'))        
        except IOError:
            pass
        
    def load(self):
        try:
            pref_dict = {}
            
            # Miscellaneous section
            pref_dict["misc"] = {}
            pref_dict["misc"]["auto-select-when-added"] = self.getboolean("misc","auto-select-when-added")
            pref_dict["misc"]["show-notifications"] = self.getboolean("misc","show-notifications")
            
            # Log section
            pref_dict["log"] = {}
            pref_dict["log"]["name"] = self.get("log","name")
            pref_dict["log"]["path"] = os.path.expanduser(self.get("log","path"))
            pref_dict["log"]["mode"] = self.get("log","mode")
            pref_dict["log"]["datetime"] = self.get("log","datetime")
            pref_dict["log"]["format"] = self.get("log","format",1)
            pref_dict["log"]["level"] = self.getint("log","level")
            
            # Tree Columns Properties           
            for column in env.COLUMN_IDS:
                pref_dict[column] = {}
                pref_dict[column]["visible"]    = self.getboolean(column,"visible")
                pref_dict[column]["editable"]   = self.getboolean(column,"editable")
                pref_dict[column]["background"] = self.get(column,"background")
                pref_dict[column]["foreground"] = self.get(column,"foreground")
            
            # Generic Tagging section
            pref_dict["generic-tag"] = {}
            pref_dict["generic-tag"]["hide-frame-property"] = self.get("generic-tag","hide-frame-property")
            pref_dict["generic-tag"]["active-at-start"] = self.getboolean("generic-tag","active-at-start")
            pref_dict["generic-tag"]["n-of-total"] = self.getboolean("generic-tag","n-of-total")
            
            # Music section
            pref_dict["music"] = {}
            pref_dict["music"]["start-folder"] = self.get("music","start-folder")
            pref_dict["music"]["player"] = self.get("music","player")
            
            # Cover section
            pref_dict["cover"] = {}
            pref_dict["cover"]["start-folder"] = self.get("cover","start-folder")
                
        except ConfigParser.NoSectionError, exc:
            print "%s" % exc
        except ConfigParser.NoOptionError, exc:
            print "%s" % exc
        except ConfigParser.ParsingError, exc:
            print "%s" % exc            
        
           
        return pref_dict
    
    def save(self,d):        
        """ Save the given configuration dictionary to the config file """
        try:
            f = open(self.configfile,'w')
            f.write(env.HEADER)            
            
            # Miscellaneous section
            self.set("misc","auto-select-when-added",d["misc"]["auto-select-when-added"])
            self.set("misc","show-notifications",d["misc"]["show-notifications"])
                        
            # Log section
            self.set("log","name",d["log"]["name"])
            self.set("log","path",d["log"]["path"])
            self.set("log","mode",d["log"]["mode"])
            self.set("log","datetime",d["log"]["datetime"])
            self.set("log","format",d["log"]["format"])
            self.set("log","level",d["log"]["level"])
            
            # Set Columns sections with its properties
            for col_id in env.COLUMN_IDS:
                try:
                    self.set(col_id,"visible",d[col_id]["visible"])
                    self.set(col_id,"editable",d[col_id]["editable"])
                    self.set(col_id,"background",d[col_id]["background"])
                    self.set(col_id,"foreground",d[col_id]["foreground"])
                except:
                    print "Critical section '%s':" % col_id
                    print "cannot write configuration..."
                    print sys.exc_value
                
            # Generic tagging section
            self.set("generic-tag","hide-frame-property",d["generic-tag"]["hide-frame-property"])
            self.set("generic-tag","active-at-start",d["generic-tag"]["active-at-start"])
            self.set("generic-tag","n-of-total",d["generic-tag"]["n-of-total"])
            
            # Music section
            self.set("music","start-folder",d["music"]["start-folder"])
            self.set("music","player",d["music"]["player"])
            
            # Cover section
            self.set("cover","start-folder",d["cover"]["start-folder"])
                             
            self.write(f)            
        except:
            print "Critital Error GMusicTagger: Saving config file..."
            print sys.exc_value
        finally:
            f.close()
                        
    def create_config(self):        
        """ Build up new config file with defaults options """
        try:
            f = open(self.configfile,'w')
            f.write(env.HEADER)
            
            # Miscellaneous section
            self.add_section("misc")
            self.set("misc","auto-select-when-added",'True')
            self.set("misc","show-notifications",'True')
                        
            # Log section
            self.add_section("log")
            self.set("log","name",env.DEFAULTS["LOG"]["name"])
            self.set("log","path",env.DEFAULTS["LOG"]["path"])
            self.set("log","mode",env.DEFAULTS["LOG"]["mode"])
            self.set("log","datetime",env.DEFAULTS["LOG"]["datetime"])
            self.set("log","format",env.DEFAULTS["LOG"]["format"])
            self.set("log","level",env.DEFAULTS["LOG"]["level"])
            
            # Set Columns sections with its properties
            for col_id in env.COLUMN_IDS:
                self.add_section(col_id)
                self.set(col_id,"visible",env.DEFAULTS["COLUMNS"][col_id]["visible"])
                self.set(col_id,"editable",env.DEFAULTS["COLUMNS"][col_id]["editable"])
                self.set(col_id,"background",env.DEFAULTS["COLUMNS"][col_id]["background"])
                self.set(col_id,"foreground",env.DEFAULTS["COLUMNS"][col_id]["foreground"])
            
            # Generic tagging section
            self.add_section("generic-tag")
            self.set("generic-tag","hide-frame-property",'visible')
            self.set("generic-tag","active-at-start",'False')
            self.set("generic-tag","n-of-total",'True')
            
            # Music section
            self.add_section("music")
            self.set("music","start-folder",env.DEFAULTS["MUSIC"]["start-folder"])
            self.set("music","player",env.DEFAULTS["MUSIC"]["player"])
            
            # Cover section
            self.add_section("cover")
            self.set("cover","start-folder",env.DEFAULTS["COVER"]["start-folder"])
                     
            self.write(f)
        except:
            print "Critital Error GMusicTagger: Creating config file..."
            print sys.exc_value
            exit(15)
        finally:
            f.close()
                              
                      
