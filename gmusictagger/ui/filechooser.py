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
import pygtk
pygtk.require('2.0')
import gtk

import core.env as env
from core.env import _


def selectMp3Files(parent=None,path=os.path.expanduser("~").decode(env.LOCALE_ENCODE)):
    """ Opens a FileChooserDialog with a mp3/m3u filter to choose one o more files
    Returns the selected files in a list """
    mp3filter = gtk.FileFilter()
    mp3filter.set_name(_("Mp3 Files"))
    mp3filter.add_pattern("*.mp3")
    mp3filter.add_pattern("*.MP3")   
    
    dialog = gtk.FileChooserDialog(_("Choose your files to edit"),
                                   parent,
                                   gtk.FILE_CHOOSER_ACTION_OPEN,
                                   (gtk.STOCK_CANCEL,gtk.RESPONSE_CANCEL,
                                    gtk.STOCK_OK,gtk.RESPONSE_OK))
    dialog.set_select_multiple(True)
    dialog.add_filter(mp3filter)
    dialog.set_current_folder(path)
    
    response = dialog.run()
    if response == gtk.RESPONSE_OK:
        selected_mp3files = dialog.get_filenames()
    else:
        selected_mp3files = []
    
    dialog.destroy()
    
    return selected_mp3files


def selectCoverFile(parent=None,path=os.path.expanduser("~").decode(env.LOCALE_ENCODE)):
    """ Opens a FileChooserDialog with an image filter to choose one file.
    Returns the selected file """
    coverfilter = gtk.FileFilter()
    coverfilter.set_name(_("Image Files"))
    coverfilter.add_pattern("*.png")
    coverfilter.add_pattern("*.PNG")
    coverfilter.add_pattern("*.jpg")
    coverfilter.add_pattern("*.JPG")
    coverfilter.add_pattern("*.jpeg")
    coverfilter.add_pattern("*.JPEG")
    coverfilter.add_pattern("*.bmp")
    coverfilter.add_pattern("*.BMP")
    
    dialog = gtk.FileChooserDialog(_("Choose your cover file"),
                                   parent,
                                   gtk.FILE_CHOOSER_ACTION_OPEN,
                                   (gtk.STOCK_CANCEL,gtk.RESPONSE_CANCEL,
                                    gtk.STOCK_OK,gtk.RESPONSE_OK))
    dialog.set_select_multiple(False)
    dialog.add_filter(coverfilter)
    dialog.set_current_folder(path)

    # Sets the Preview Image Widget
    preview = gtk.Image()
    dialog.set_preview_widget(preview)
    dialog.set_use_preview_label(False)
    dialog.connect("update-preview", update_preview_cb, preview)
    
    response = dialog.run()
    if response == gtk.RESPONSE_OK:
        selected_cover = dialog.get_filename()
    else:
        selected_cover = ""
    
    dialog.destroy()
    
    return selected_cover
                                    

def update_preview_cb(file_chooser, preview):
    filename = file_chooser.get_preview_filename()
    try:
        pixbuf = gtk.gdk.pixbuf_new_from_file_at_size(filename,
                                                      env.APIC_WIDTH,
                                                      env.APIC_HEIGHT)
        preview.set_from_pixbuf(pixbuf)
        have_preview = True
    except:
        have_preview = False
    
    file_chooser.set_preview_widget_active(have_preview)
    

def saveCoverFileAs(parent=None,
                    path=os.path.expanduser("~").decode(env.LOCALE_ENCODE),
                    filename="Mp3Cover.jpg"):
    """
    Opens a filechooser dialog to set the name of the image to save
    """
    dialog = gtk.FileChooserDialog(_("Save you cover as..."),
                                   parent,
                                   gtk.FILE_CHOOSER_ACTION_SAVE,
                                   (gtk.STOCK_CANCEL,gtk.RESPONSE_CANCEL,
                                    gtk.STOCK_OK,gtk.RESPONSE_OK))
    dialog.set_current_folder(path)
    dialog.set_current_name(filename)
    
    response = dialog.run()
    if response == gtk.RESPONSE_OK:
        cover_save_as = dialog.get_filename()
    else:
        cover_save_as = ""
    
    dialog.destroy()
    
    return cover_save_as 
    
