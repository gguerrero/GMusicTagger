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
import logging
import copy
import eyeD3
import time

import pygtk
pygtk.require('2.0')
import gtk


import core.env as env
from core.env import _
import core.mp3storage as mp3storage

import ui.message as message
import ui.listmodel as listmodel

# Sets logger
APPLOG = logging.getLogger(__name__)

# All tree tooltip
MP3TREE_TOOLTIP_MARKUP = _("""<b><i>Drop</i></b> files or directories in the tree to load Mp3 Files.
<b><i>Select/Unselect</i></b> the mp3 file by toggling the check button on its column.
<b><i>Click</i></b> on any field to edit it.""")

# Cancel Action sleep time
CANCEL_ACTION_SLEEP = 2.0

class Mp3Tree(gtk.TreeView):
    def __init__(self, app_config):
        gtk.TreeView.__init__(self)        
        self.get_selection().set_mode(gtk.SELECTION_SINGLE)
        self.set_tooltip_markup(MP3TREE_TOOLTIP_MARKUP)
        
        # Publicate the Application Configuration
        self.config = app_config
        
        # Create the Mp3 Storage
        self.mp3_store = mp3storage.Mp3Storage()
                
        # Set View and Model
        self.__set_view_and_model()
                        
        # Set TreeView Properties
        self.set_enable_search(True)
        self.set_search_column(env.COLUMN_ID_INDEX['FILE']) 
                              
        # Show Treeview
        self.show()   
    
    def share_attributes(self, **kwargs):
        """
        For each parameter pair given, create an internal attribute
        with full control 
        """
        for key,value in kwargs.items():
            try:
                setattr(self,key,value)
            except:
                APPLOG.error("Cannot create attribute %s" % key)
               
    def __set_view_and_model(self):
        """ Sets the Tree columns """
        
        # Column types list
        column_types = []
        
        # Sets each colum as its type
        for column in env.MP3TREE_COLUMNS:
            # Extract values
            column_id = column['col_id']
            column_type = column['type']
            column_index = column['index']
            column_name = column['name']
            
            # Set the column renderer and its properties, gets the TreeViewColumn
            if column_type == str:
                column_renderer = gtk.CellRendererText()
                column_renderer.set_property('editable', self.config[column_id]['editable'])
                column_renderer.set_property('background', self.config[column_id]['background'])
                column_renderer.set_property('foreground', self.config[column_id]['foreground'])
                column_renderer.connect('edited',self.__on_text_renderer_edited,column_index)
                
                treeview_column = gtk.TreeViewColumn(column_name,column_renderer,text=column_index)            
                 
            elif column_type == bool:
                column_renderer = gtk.CellRendererToggle()
                column_renderer.connect('toggled',self.__on_renderer_track_selection_column_toggled,column_index)
                
                treeview_column = gtk.TreeViewColumn(column_name,column_renderer,active=column_index)            
                
            elif column_type == object:
                # Append manually the string renderer type before the object type                
                column_types.append(str)
                
                self.genre_model = listmodel.GenreListStore()
                                           
                column_renderer = gtk.CellRendererCombo()
                column_renderer.set_property('editable', self.config[column_id]['editable'])      
                column_renderer.set_property('model', self.genre_model)
                column_renderer.set_property('text-column', 0)
                column_renderer.set_property('has-entry', True)
                column_renderer.set_property('background', self.config[column_id]['background'])
                column_renderer.set_property('foreground', self.config[column_id]['foreground'])
                column_renderer.connect('edited', self.__on_text_renderer_edited,column_index)       
            
                treeview_column = gtk.TreeViewColumn(column_name,column_renderer,text=column_index)                 
            
            # Append column type for the ListStore Model
            column_types.append(column_type)     
                
            # Set the TreeViewColumn Properties            
            treeview_column.set_resizable(True)
            if column_id == 'SELEC':
                treeview_column.set_property('visible',True)                
            else:
                treeview_column.set_property('visible',self.config[column_id]['visible'])
            
            # Append the new column to the TreeView
            self.append_column(treeview_column)          

        # Sets the tree model
        self.model = gtk.ListStore(*column_types)
        self.set_model(self.model)   
             
    def __update_column_properties(self,column_id):
        """
        Based on the new configuration, update all the column properties like
        visible, background and foreground
        """
        try:
            APPLOG.info("Updating %s column properties" % column_id)
            
            column = self.get_column(env.COLUMN_ID_INDEX[column_id])
            renderer_list = column.get_cell_renderers()
            for renderer in renderer_list:
                renderer.set_property('background',
                                      self.config[column_id]['background'])
                renderer.set_property('foreground',
                                      self.config[column_id]['foreground'])                                      
            column.set_property('visible',self.config[column_id]['visible'])
        except:
            APPLOG.exception("Error updating %s column properties" % column_id)
          
    def update_properties(self, new_config):
        """
        Update all the tree column properties
        """
        self.config = new_config
        for col_id in env.COLUMN_IDS:
            self.__update_column_properties(col_id)
        self.grab_focus()
       
    ###########################################################################
    ## Tree Signal Methods
                   
    def __on_text_renderer_edited(self,renderer,path,new_value,column):
        """ Checks if the column iter value change is value and set it """
        APPLOG.debug("Text renderer edited at (%s,%s): %s" % (path,column,new_value))
        liststore = self.get_model()
        actual_iter = liststore.get_iter(path)
        actual_value = liststore.get_value(actual_iter,column)
        
        if actual_value != new_value:
            # Edit the Mp3 Tag with the new value on the Frame
            mp3_path = self.get_active_row_mp3_path()
            if mp3_path:
                # With the text and the column edit the Mp3 Frame
                column_id = self.__get_column_id(column)
                is_updated = self.__update_mp3_frame_with(mp3_path,
                                                          column_id,
                                                          new_value)
                
                if is_updated:                                            
                    # Mark the track with to be updated
                    self.mp3_store.set_for_update(mp3_path)

                    # Sets the new value on the cell
                    liststore.set(actual_iter,
                                  column,
                                  new_value)

    def __get_column_id(self, column_number):
        """
        Gets the Mp3 Frame to updated by using the column number and
        the enviroments dictionary.
        """
        column_id = ""
        for col_id,col_num in env.MODEL_ID_INDEX.items():
            if col_num == column_number:
                column_id = col_id
                break
        
        return column_id
                                         
    def __update_mp3_frame_with(self,mp3_path,column_id,frame_text):
        """
        No change are made if the column is the FileName. This always will
        be a post 'eyeD3.Tag.update()' change. Just rename the file when the
        save button is clicked.
        """
        APPLOG.info("Update %s frame on %s" % (column_id,mp3_path))
        is_updated = True
        
        try:                      
            if column_id == 'FILE':
                # Do not edit the file name with blank
                if frame_text == "":
                    is_updated = False
                else:
                    self.mp3_store.set_mp3_rename_with(mp3_path,frame_text)                    
            else:
                # Gets the mp3 tag
                mp3_audio_file = self.mp3_store.get_metadata(mp3_path)
                mp3_tag = mp3_audio_file.getTag() 
                
                        
                # Evaluate the column ID to change the Mp3 Frame.
                # No 'case' statement on Python :(
                if column_id == 'TRCK':
                    tracknum = self.getTrackNumTuple(frame_text)
                    if tracknum:
                        mp3_tag.setTrackNum(tracknum)
                    else:
                        is_updated = False
                elif column_id == 'TIT2':
                    mp3_tag.setTitle(frame_text)
                elif column_id == 'TPE1':
                    mp3_tag.setArtist(frame_text,'TPE1')
                elif column_id == 'TPE2':
                    mp3_tag.setArtist(frame_text,'TPE2')
                elif column_id == 'TPE3':
                    mp3_tag.setArtist(frame_text,'TPE3')
                elif column_id == 'TPE4':
                    mp3_tag.setArtist(frame_text,'TPE4')
                elif column_id == 'TCOM':
                    mp3_tag.setArtist(frame_text,'TCOM')
                elif column_id == 'TALB':
                    mp3_tag.setAlbum(frame_text)
                elif column_id == 'TYER':
                    if frame_text.isdigit() or not frame_text:
                        mp3_tag.setDate(frame_text)
                    else:
                        is_updated = False
                elif column_id == 'TCON':
                    mp3_tag.setGenre(frame_text)
                elif column_id == 'COMM':
                    mp3_tag.removeComments()
                    mp3_tag.addComment(frame_text)
                else:
                    is_updated = False 
        except:
            APPLOG.exception("Critical Error while updating Mp3 %s frame" % mp3_path)
            is_updated = False
                
        return is_updated
        
    def __on_renderer_track_selection_column_toggled(self,renderer,path,column):
        """ Just set selectall button to inconsistent state if this one is toggled """
        APPLOG.debug("Toggle renderer at (%s,%s)" % (path,column))
        liststore = self.get_model()
        actual_iter = liststore.get_iter(path)
        actual_value = liststore.get_value(actual_iter,column)
        liststore.set(actual_iter,column, not actual_value)
        
        if self.cbtn_selectall.get_active():
            self.cbtn_selectall.set_inconsistent(True)               
    
    
    ###########################################################################


    ###########################################################################
    ## Adding tracks methods
                
    def getTrackNumString(self, tracknum_tuple):
        """ Return the mp3 track number tuple
        formatted as n/n """
        tracknum_string = ""
        if tracknum_tuple[0]:
            tracknum_string = str(tracknum_tuple[0])        
        if tracknum_tuple[1]:
            tracknum_string = "%s/%s" % (tracknum_string,
                                         str(tracknum_tuple[1]))
        return tracknum_string
    
    def getTrackNumTuple(self,tracknum_string):
        """ Return the mp3 track number string
        formatted as a tuple: (n,n) """
        tracknum_list = tracknum_string.strip().split("/")[:2]
        
        for i in range(len(tracknum_list)): tracknum_list[i] = tracknum_list[i].strip()
        if tracknum_list[0] == '': tracknum_list[0] = None
        if len(tracknum_list) == 1: tracknum_list.append(None)        
        
        if (not tracknum_list[0] or tracknum_list[0].isdigit()) and \
           (not tracknum_list[1] or tracknum_list[1].isdigit()):
            tracknum_tuple = tuple(tracknum_list)            
        else:
            tracknum_tuple = None                
        
        return tracknum_tuple
            
                                             
    def add_iters(self,mp3_files):
        """ Insert the new mp3 files in the Tree ListStore """
        APPLOG.info("Add new iters on the Mp3 Tree")
        
        # Initialize addition counter
        total_files_added = 0
        
        # Initialize the progressbar
        self.progressbarbox.set_property('visible',True)
        self.progressbarbox.set_new_bar(len(mp3_files))
                                     
        # Append the files in the Tree ListStore
        for mp3 in mp3_files:
            # Check if the action is not cancelled            
            if not self.progressbarbox.cancel_action:
                # Refresh the progressbar
                self.progressbarbox.next(_("Loading %s...") % mp3)
            
                # Add Mp3 File in the storage Core and read it
                added_mp3 = self.mp3_store.add_item(mp3)
                if added_mp3:
                    if added_mp3 < 2:
                        try:
                            mp3_audio_file = self.mp3_store.get_metadata(mp3)
                            mp3_tag = mp3_audio_file.getTag() 
                            
                            # Gets Filename by the path basename and without ext
                            filename = os.path.basename(mp3)
                            i = filename.rindex('.')
                            filename = filename[:i]
                            
                            # Retrieve the complex tags (Genre and Comments)
                            try:
                                genre = mp3_tag.getGenre()
                                if genre:
                                    genre_name = genre.getName()
                                else:
                                    genre_name = u''
                            except eyeD3.tag.GenreException:
                                genre_name = ''
                                                
                            comments = mp3_tag.getComments()
                            if len(comments) > 0:
                                comment_string = comments[0].comment
                            else:
                                comment_string = u''                         
                            
                            
                            # Retrieve all text fields of the MP3 tag
                            # and sets the tree fields
                            col_selec      = self.config['misc']['auto-select-when-added']
                            col_file       = filename
                            col_num        = self.getTrackNumString(mp3_tag.getTrackNum())
                            col_title      = mp3_tag.getTitle()
                            col_artist     = mp3_tag.getArtist('TPE1')
                            col_band       = mp3_tag.getArtist('TPE2')
                            col_performer  = mp3_tag.getArtist('TPE3')
                            col_remix      = mp3_tag.getArtist('TPE4')
                            col_compositor = mp3_tag.getArtist('TCOM')
                            col_album      = mp3_tag.getAlbum()
                            col_year       = mp3_tag.getYear()
                            col_genre      = genre_name
                            col_comments   = comment_string
                            col_duration   = mp3_audio_file.getPlayTimeString()
                            col_bitrate    = mp3_audio_file.getBitRateString()
                            col_path       = mp3
                            
                            iter_tuple_values = (col_selec, col_file, col_num, col_title,
                                                 col_artist, col_band, col_performer,
                                                 col_remix, col_compositor, col_album,
                                                 col_year, col_genre, self.genre_model,
                                                 col_comments, col_duration, col_bitrate,
                                                 col_path)                                     

                            self.model.append(iter_tuple_values)
                            total_files_added += 1
                        except:
                            APPLOG.exception("Reading Tag from %s" % mp3)
                            message.exception(_("Reading Mp3 tags"),
                                              _("Error reading Mp3 Tag from '%s'\n")
                                              % os.path.basename(mp3).replace("&","&amp;"),
                                              self.get_toplevel())
                            self.mp3_store.remove_items([mp3])                        
                else:          
                    message.error(_("Initialize Mp3 Tag"),
                                  _("Error adding Mp3 File '%s'.\nCheck the app log.")
                                  % os.path.basename(mp3).replace("&","&amp;"),
                                  self.get_toplevel())  
            else:
                APPLOG.warning("Load process cancelled")
                self.progressbarbox.cancel_message()
                time.sleep(CANCEL_ACTION_SLEEP)
                break
                        
        # Hide the progressbar
        self.progressbarbox.set_property('visible',False)
                                              
        return total_files_added

    ###########################################################################


    ###########################################################################
    ## Remove tracks methods
    
    def remove_selected_iters(self):
        """
        Remove the all the seleted mp3 Files on the tree.
        The selected files should be checked
        """        
        selected_iters = self.get_selected_iters()
        for mp3iter in selected_iters:
            mp3path = self.model.get_value(mp3iter,
                                           env.MODEL_ID_INDEX['PATH'])        
            self.model.remove(mp3iter)
            self.mp3_store.remove_item(mp3path)
            
    def remove_iters(self, mp3_files):
        """ Remove the mp3 files (as path) of the Tree ListStore """
        mp3_iters_to_remove = []
        self.model.foreach(self.__add_iter_if_exists_on,(mp3_files,mp3_iters_to_remove))
        for mp3_iter in mp3_iters_to_remove:           
            self.model.remove(mp3_iter)
            
        return mp3_files
        
    def __add_iter_if_exists_on(self, liststore, path, mp3_iter, (mp3_list_to_remove,mp3_iters_to_remove)):
        """ Add the iter in a list if its path is 
        in the mp3 list given (same as check is selected) """
        mp3_path = liststore.get_value(mp3_iter,
                                       env.MODEL_ID_INDEX['PATH'])
        if mp3_path in mp3_list_to_remove:
            mp3_iters_to_remove.append(mp3_iter)
            mp3_list_to_remove.remove(mp3_path)

    ###########################################################################
    
    
    ###########################################################################
    ## Misc methods

    def is_any_row_active(self):
        """
        Return True if any row is active,
        otherwise return False
        """
        model,selected_iter = self.get_selection().get_selected()
        if selected_iter:
            row_active = True
        else:
            row_active = False
        
        return row_active
            
    def get_active_row_mp3_path(self):
        """
        From the active row, gets the mp3 full path
        """
        # Extract the path on the selected row        
        liststore, selected_iter = self.get_selection().get_selected()
        if selected_iter:
            mp3_path = liststore.get_value(selected_iter,
                                           env.MODEL_ID_INDEX['PATH'])
        else:
            mp3_path = None
        
        return mp3_path     
                                                                            
    def get_selected_mp3_files(self):
        """ Return a list with the selected Mp3 Files """
        selected_iters = self.get_selected_iters()
        selected_mp3_files = []
        for mp3iter in selected_iters:
            mp3path = self.model.get_value(mp3iter,
                                           env.MODEL_ID_INDEX['PATH'])
            selected_mp3_files.append(mp3path)
                        
        return selected_mp3_files
                
    def get_selected_iters(self):
        """
        Return a list with the iters that are checked
        """
        selected_iters = []
        self.model.foreach(self.__append_if_selected,selected_iters)
        
        return selected_iters
            
    def __append_if_selected(self, liststore, path, actual_iter, selected_iters):
        """ Append the iter in the selected iter list 
        if this iter have the selection column checked """
        is_iter_selected = liststore.get_value(actual_iter,
                                               env.MODEL_ID_INDEX['SELEC'])
        if is_iter_selected: selected_iters.append(actual_iter)                                          

    def select_all(self):
        """ """
        self.model.foreach(self.__change_status_mp3_iter,True)
                       
    def unselect_all(self):
        """ """
        self.model.foreach(self.__change_status_mp3_iter,False)
        
    def __change_status_mp3_iter(self, liststore, path, mp3_iter, is_active): 
        """ Change the selection column status of an iter to 'is_active' value """
        liststore.set(mp3_iter,
                      env.MODEL_ID_INDEX['SELEC'],
                      is_active)

    def update_mp3_path(self, old_mp3_path, new_mp3_path):
        """ Search and change the path column text """
        self.model.foreach(self.__update_path_column_if,(old_mp3_path,new_mp3_path))
        
    def __update_path_column_if(self, liststore, path, actual_iter, (old_mp3_path,new_mp3_path)):
        """ Change the path column text if the old mp3 path matches """
        this_path_value = liststore.get_value(actual_iter,
                                              env.MODEL_ID_INDEX['PATH'])
        if this_path_value == old_mp3_path:
            liststore.set_value(actual_iter,
                                env.MODEL_ID_INDEX['PATH'],
                                new_mp3_path)
                                                      
    ###########################################################################
    
                          
    ###########################################################################
    ## Move up/down the active tree row
                      
    def move_track_up(self):
        """ 
        Get the actual iter path to move it one path up.
        Caution! If tree is sorted this method won't work
        """
        APPLOG.debug("Move up the selected track on the tree")
        model,active_iter = self.get_selection().get_selected()
        if active_iter:      
            try:
                path = model.get_path(active_iter)            
                if path[0] > 0:
                    previous_path = (path[0]-1,)
                    previous_iter = model.get_iter(previous_path)
                    model.move_before(active_iter,previous_iter)
            except ValueError, exc:
                APPLOG.warning("No more row to set up with. Row already set on top")
        
    def move_track_down(self):
        """
        Get the actual iter path to move it one path down 
        Caution! If tree is sorted this method won't work
        """
        APPLOG.debug("Move down the selected track on the tree")                       
        model,active_iter = self.get_selection().get_selected()
        if active_iter:  
            try:
                path = model.get_path(active_iter)            
                next_path = (path[0]+1,)
                next_iter = model.get_iter(next_path)
                model.move_after(active_iter,next_iter)
            except ValueError, exc:
                APPLOG.warning("No more row to set down with. Row already set at the bottom")

    ###########################################################################


    ###########################################################################
    ## APIC various methods
    
    def get_active_row_mp3_apic_filename(self):
        """
        Return a posible filename for the APIC of and mp3 based on the Mp3 file
        name and in the APIC mimeType (to get the filename extension)
        """
        APPLOG.debug("construct the APIC filename from the Mp3")
        mp3_path = self.get_active_row_mp3_path()
        if mp3_path:          
            # Get the Mp3 name without extension
            mp3_filename = os.path.basename(mp3_path)
            i = mp3_filename.rindex(".")
            mp3_filename = mp3_filename[:i]
            
            # Get the APIC extension
            apic_extension = self.mp3_store.get_apic_file_extension(mp3_path)
            
            # Get APIC Filename
            apic_filename = mp3_filename + apic_extension            
        else:
            APPLOG.warning("No Mp3 row selected")
            apic_filename = "Mp3Cover.jpg"
        
        return apic_filename
        
    def export_active_row_mp3_apic_as(self,apic_path):
        """
        Export the active row mp3 apic with the apic_path name
        """
        APPLOG.debug("Export the Mp3 APIC to a File")
        mp3_path = self.get_active_row_mp3_path()
        if mp3_path:
            self.mp3_store.export_apic_as(mp3_path,apic_path)
        
    def get_active_row_mp3_apic(self):
        """
        Extract and return the active iter APIC Frame if exists
        """
        APPLOG.debug("get the selected mp3 row APIC")
        apic_pixbuf = None
        
        # Extract the path on the selected row        
        liststore, selected_iter = self.get_selection().get_selected()
        if selected_iter:
            mp3_path = liststore.get_value(selected_iter,
                                           env.MODEL_ID_INDEX['PATH'])
                                           
            apic_pixbuf = self.mp3_store.get_apic_pixbuf(mp3_path)
                                    
        return apic_pixbuf
    
    def set_apic_on_active_row_mp3(self,apic_path):
        """
        Apply the selected cover file on the mp3 active row.
        """        
        # Extract the path on the selected row        
        liststore, selected_iter = self.get_selection().get_selected()
        if selected_iter:
            mp3_path = liststore.get_value(selected_iter,
                                           env.MODEL_ID_INDEX['PATH'])
                                           
            apic_is_updated = self.mp3_store.set_apic(mp3_path, apic_path)                          
            if apic_is_updated:
                self.mp3_store.set_for_update(mp3_path)     
            else:
                APPLOG.warning("Any updates on the Mp3 APIC")                    
                
    def remove_appic_from_active_row_mp3(self):
        """
        Remove the actual Mp3 APIC
        """
        APPLOG.debug("Remove the Mp3 APIC")
        mp3_path = self.get_active_row_mp3_path()
        if mp3_path:
            apic_is_removed = self.mp3_store.remove_apic(mp3_path)
            if apic_is_removed:
               self.mp3_store.set_for_update(mp3_path) 
                
    ###########################################################################
    
        
    ###########################################################################
    ## Update tracks methods    
    def update_selected_iters(self):
        """
        Retrieve all the mp3 paths selected with changes pending to update 
        and update them tags. Rename the files if File column have changes.
        """
        APPLOG.info("Update selected mp3 paths with pending changes")
        
        # Initialize updates counter
        total_files_updated = 0        
        
        # Gets the mp3 paths to update        
        selected_mp3_paths = self.get_selected_mp3_files()
        mp3_paths_to_update = self.mp3_store.pending_files_to_update(selected_mp3_paths)
        
        if mp3_paths_to_update:                   
            # Initialize the progressbar
            self.progressbarbox.set_property('visible',True)
            self.progressbarbox.set_new_bar(len(mp3_paths_to_update))
                    
            for mp3 in mp3_paths_to_update:
                # Check if the action is not cancelled            
                if not self.progressbarbox.cancel_action:
                    # Refresh the progressbar
                    self.progressbarbox.next(_("Updating %s...") % mp3)                 
                
                    # Update Mp3 tag and rename the filename
                    is_updated = self.mp3_store.update(mp3)
                    
                    # Rename Mp3 file
                    is_renamed = False
                    new_mp3 = self.mp3_store.rename(mp3)
                    if new_mp3:
                        is_renamed = True
                        if mp3 != new_mp3:                        
                            self.update_mp3_path(mp3,new_mp3)
                            mp3 = new_mp3
                                                            
                    if is_updated and is_renamed:
                        self.mp3_store.remove_for_update(mp3)
                        APPLOG.info("'%s' successfully saved" % mp3)                        
                        total_files_updated += 1                                                
                    elif not is_updated:
                        APPLOG.info("'%s' not saved" % mp3)
                        message.error(_("Save Mp3 changes"),
                                      _("Error while saving Mp3 %s metadata") % mp3,
                                      self.get_toplevel())
                    elif not is_renamed:
                        APPLOG.info("'%s' not renamed" % mp3)
                        message.error(_("Save Mp3 changes"),
                                      _("Error while renaming Mp3 %s") % mp3,
                                      self.get_toplevel())
                else:
                    APPLOG.warning("Save process cancelled")
                    self.progressbarbox.cancel_message()
                    time.sleep(CANCEL_ACTION_SLEEP)
                    break           
                
            # Hide the progressbar
            self.progressbarbox.set_property('visible',False)                                                              
        else:
            APPLOG.info("No changes pending on the selected mp3 files")
            message.info(_("Update Mp3 files"),
                         _("No changes pending on the selected Mp3 Files."),
                         self.get_toplevel())

        return total_files_updated
                              
    ###########################################################################   


    ###########################################################################   
    ## Generic tag methods
    
    def get_frame_pattern_text(self, mp3_iter, string_to_parse):
        """
        From a string with pattern like %artist, %title or %trck parse it with
        the iter correspondent column text (artis, title or tracknum). Then
        return the new created string.
        """
                
        # Check each pattern frame association
        for frame_pattern, frame_id in env.MP3FRAME_PATTERN.items():
            if frame_pattern in string_to_parse:
                frame_text = self.model.get_value(mp3_iter,
                                                  env.MODEL_ID_INDEX[frame_id])                
                string_to_parse = string_to_parse.replace(frame_pattern,
                                                          frame_text)
                

        # Replace not allowed filename characters with '_'
        for invalid_char in env.INVALID_FILENAME_CHARS:
            if invalid_char in string_to_parse:
                string_to_parse = string_to_parse.replace(invalid_char,'_')

        return string_to_parse

    def get_album_trck_report(self, mp3_iters):
        """
        Extract the album from each iter to create the album report.
        The Album report will contain for each album found in the iters, the
        total number of tracks composing that album and a sequence initilize
        with zero.
        """
        report = {}
        for mp3_iter in mp3_iters:
            album = self.model.get_value(mp3_iter,
                                         env.MODEL_ID_INDEX['TALB'])
            if report.has_key(album):
                report[album]['total'] += 1
            else:
                report[album] = {}
                report[album]['total'] = 1
                report[album]['seq'] = 1
        
        return report
            
    def apply_generic_tag_on_selected(self, generic_tag_values):
        """
        Get the selected iters on the tree. Apply the generic tag given
        values to each selected iter.
        """
        
        # Retrieve the Mp3 select iter on the Mp3 Tree
        mp3_selected_iters = self.get_selected_iters()
        
        # Extract tracknum sequence and delete tracknum options
        delete_tracknum = False
        create_sequence = False
        
        if generic_tag_values.has_key('DELTRCK'):
            delete_tracknum = generic_tag_values.pop('DELTRCK')        

        if generic_tag_values.has_key('TRCKSEQ'):
            create_sequence = generic_tag_values.pop('TRCKSEQ')
            
            if create_sequence and not delete_tracknum:
                album_trck_report = {}
                if generic_tag_values.has_key('TALB'):                
                    generic_album = generic_tag_values['TALB']
                    album_trck_report[generic_album] = {}
                    album_trck_report[generic_album]['total'] = len(mp3_selected_iters)
                    album_trck_report[generic_album]['seq'] = 1
                else:
                    album_trck_report = self.get_album_trck_report(mp3_selected_iters)
  
        # Extract compact artist option
        compact_artist = False
        if generic_tag_values.has_key('COMPACT'):
            compact_artist = generic_tag_values.pop('COMPACT')        
        
        # Extract FILE frame to apply after the frame dependencies
        file_frame_pattern = None
        if generic_tag_values.has_key('FILE'):
            file_frame_pattern = generic_tag_values.pop('FILE')
        
        # Extract APIC frame
        is_generic_APIC = False
        generic_APIC = None
        if generic_tag_values.has_key('APIC'):
            is_generic_APIC = True
            generic_APIC = generic_tag_values.pop('APIC')
        
        
        # For each selected iter on the Mp3 Tree...        
        for mp3_iter in mp3_selected_iters:
            # Get the Mp3 Path
            mp3_path = self.model.get_value(mp3_iter,
                                            env.MODEL_ID_INDEX['PATH'])
            
            # Apply each Frame Text
            for frame_id,frame_text in generic_tag_values.items():                
                # Update the eyeD3 tag of the Mp3 File
                is_updated = self.__update_mp3_frame_with(mp3_path,
                                                          frame_id,frame_text)            
                if is_updated:
                    # Mark the track with to be updated
                    self.mp3_store.set_for_update(mp3_path)

                    # Sets the new value on the cell
                    self.model.set(mp3_iter,
                                   env.MODEL_ID_INDEX[frame_id],
                                   frame_text)

            # The 'APIC' frame
            if is_generic_APIC:
                if generic_APIC:
                    apic_is_updated = self.mp3_store.set_apic(mp3_path, generic_APIC)                          
                    if apic_is_updated:
                        self.mp3_store.set_for_update(mp3_path)                     
                else:
                    apic_is_removed = self.mp3_store.remove_apic(mp3_path)
                    if apic_is_removed:
                        self.mp3_store.set_for_update(mp3_path)                 
                                                    
            # Compact the artist Frames
            if compact_artist:
                if self.__update_mp3_frame_with(mp3_path,'TPE2','') and \
                   self.__update_mp3_frame_with(mp3_path,'TPE3','') and \
                   self.__update_mp3_frame_with(mp3_path,'TPE4','') and \
                   self.__update_mp3_frame_with(mp3_path,'TCOM',''):
                
                    self.model.set(mp3_iter,env.MODEL_ID_INDEX['TPE2'],'')
                    self.model.set(mp3_iter,env.MODEL_ID_INDEX['TPE3'],'')
                    self.model.set(mp3_iter,env.MODEL_ID_INDEX['TPE4'],'')
                    self.model.set(mp3_iter,env.MODEL_ID_INDEX['TCOM'],'')
                
                    self.mp3_store.set_for_update(mp3_path)
                    
            # Upstream sequence for Tracknum (each album restart the seq)            
            if create_sequence and not delete_tracknum:
                iter_album = self.model.get_value(mp3_iter,
                                                  env.MODEL_ID_INDEX['TALB'])
                                                                                     
                if self.config['generic-tag']['n-of-total']:
                    tracknum_frame = str(album_trck_report[iter_album]['seq']) + \
                                     "/" + \
                                     str(album_trck_report[iter_album]['total'])
                else:
                    tracknum_frame = str(album_trck_report[iter_album]['seq'])
                 
                album_trck_report[iter_album]['seq'] += 1
                
                is_updated = self.__update_mp3_frame_with(mp3_path,
                                                          'TRCK',
                                                          tracknum_frame)
                if is_updated:
                    self.model.set(mp3_iter,
                                   env.MODEL_ID_INDEX['TRCK'],
                                   tracknum_frame)
                
                    self.mp3_store.set_for_update(mp3_path)
                
            # Delete Tracknum (not many sense if Upstream sequence was active...)
            if delete_tracknum:
                self.__update_mp3_frame_with(mp3_path,'TRCK','')
                self.model.set(mp3_iter,env.MODEL_ID_INDEX['TRCK'],'')
                
                self.mp3_store.set_for_update(mp3_path)

            # The 'FILE' frame applied after all the frame dependencies
            if file_frame_pattern:
                # Parse the frame patterns (%trck, %artist, %title...)
                frame_text = self.get_frame_pattern_text(mp3_iter,
                                                         file_frame_pattern)
                # Update the eyeD3 tag of the Mp3 File
                is_updated = self.__update_mp3_frame_with(mp3_path,
                                                          'FILE',
                                                          frame_text)           
                if is_updated:
                    # Mark the track with to be updated
                    self.mp3_store.set_for_update(mp3_path)

                    # Sets the new value on the cell
                    self.model.set(mp3_iter,
                                   env.MODEL_ID_INDEX['FILE'],
                                   frame_text) 
                                
    ###########################################################################   
        
    
    ###########################################################################   
    ## Linker methods
        
    def is_any_pending_to_update(self):
        """ Linker to mp3_store method """
        return self.mp3_store.is_any_pending_to_update()
    
    def pending_to_update(self, mp3):
        """ Linker to mp3 store method """
        return self.mp3_store.pending_to_update(mp3)
        
    def pending_files_to_update(self, mp3_files):
        """ Linker to mp3 store method """
        return self.mp3_store.pending_files_to_update(mp3_files)
    
    ###########################################################################
       
