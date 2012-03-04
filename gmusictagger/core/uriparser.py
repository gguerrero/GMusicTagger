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
import re
import urllib


def get_mp3_files_from_uri_data(data):
    """
    From a text with one or more uri descriptor(s) get the Mp3 Files
    as a normal path description. Also search in the folder if the param
    'search_in_folders' indicates to do so.
    """
    mp3_file_type    = r'\.(mp3|MP3)$'
    uri_starts_with  = r'^file:///'
    uri_replace_with = '/'
    mp3files = []
    
    data_list = data.splitlines()
    
    # Each uri get in the list
    for uri in data_list:
    
        # Convert the url chars into path normal chars
        path = urllib.url2pathname(uri)
            
        # Remove the url start (tipically 'file:///' from nautilus) 
        path = re.sub(uri_starts_with, 
                     uri_replace_with,
                     path)
        
        # If the path is a directory search inside for Mp3 files
        if os.path.isdir(path):
            for (path,dirs,files) in os.walk(path):
                files.sort()
                for f in files:
                    if re.search(mp3_file_type, f):
                        mp3 = os.path.join(path,f)
                        mp3files.append(mp3)
                                                
        # If the file is an Mp3 File and exist just add it to the list
        elif re.search(mp3_file_type, path) and os.path.isfile(path):
            mp3 = path
            mp3files.append(mp3)
 
    return mp3files
    
