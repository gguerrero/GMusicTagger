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

import copy
import eyeD3

import pygtk
pygtk.require('2.0')
import gtk

class GenreListStore(gtk.ListStore):
    """
    Define a ListStore gtk model with the eyeD3 genre list
    ordered from A to Z and removing all the 'Unknown' genres
    """
    def __init__(self):
        """ Sets the model with the actual valid ID3 genres """
        # Build a model with one String column
        gtk.ListStore.__init__(self, str)
        
        # Extract and sort the eyeD3 genre list 
        genre_list = copy.copy(eyeD3.genres)
        genre_list.sort()
        
        # Remove the "Unknown"s genres
        unknown_count = genre_list.count("Unknown")
        for i in range(0,unknown_count):
            genre_list.remove("Unknown")
        
        # Append each genre to the list
        for genre in genre_list:
            self.append([genre])
              

class FilenameListStore(gtk.ListStore):
    """
    Define a ListStore gtk model with some filename patterns for
    renameming the Mp3 files composed from internal frame fields like
    the artist (%artist), the title (%title) or the track number (%trck)
    """
    def __init__(self):
        # Build a model with one String column
        gtk.ListStore.__init__(self, str)
     
        # The model list
        model_list = ['%trck %artist - %title',
                      '%trck. %artist - %title',
                      '%trck %title - %artist',
                      '%artist - %title',
                      '%album - %title',
                      '%trck. %title (%artist)',
                      '%trck. %album[%artist] - %title']
        
        # Append each filename to the list
        for filename in model_list:
            self.append([filename])
            
