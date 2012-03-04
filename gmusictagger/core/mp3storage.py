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
import eyeD3
import logging

import pygtk
pygtk.require('2.0')
import gtk

import core.env as env

# Sets logger
APPLOG = logging.getLogger(__name__)

class Mp3Storage:
    
    # Storage Attributes
    mp3items    = {}
    mp3toupdate = []
    
    def __init__(self):
        """ Initialize MP3 storage """
        pass

    ###########################################################################
    ## Add/Remove/Update/Rename Methods
    
    def store_new_mp3(self, mp3filename):
        """
        Create a new instance for the Mp3 filename given into the mp3items dict.
        """
        mp3_metadata = eyeD3.Mp3AudioFile(mp3filename)
                                
        # If the file has no Tag...
        if not mp3_metadata.tag:
            APPLOG.warning("MP3 File has no Tag, creating a new one")
            tag = eyeD3.Tag()
            tag.setVersion(eyeD3.tag.ID3_DEFAULT_VERSION)
            tag.linkedFile = eyeD3.LinkedFile(mp3filename)
            mp3_metadata.tag = tag
        
        # Update to ID3_DEFAULT_VERSION if actual is under ID3_V2
        # Specific update for the ID3_V2_2 tag version also, because the eyeD3
        # raise TagException with "Unable to write ID3 v2.2". :(
        if mp3_metadata.tag.getVersion() <= eyeD3.tag.ID3_V2_2:
            APPLOG.warning("Updating ID3 tag %s to the eyeD3 ID3_DEFAULT_VERSION(%i)" %\
                           (mp3_metadata.tag.getVersionStr(),
                            eyeD3.tag.ID3_DEFAULT_VERSION))
            mp3_metadata.tag.setVersion(eyeD3.tag.ID3_DEFAULT_VERSION)    
                                               
        # Assign metadata to the mp3 file
        self.mp3items[mp3filename] = {}
        self.mp3items[mp3filename]['metadata'] = mp3_metadata
        self.mp3items[mp3filename]['apic_pixbuf'] = self.extract_apic_pixbuf(mp3_metadata)
        self.mp3items[mp3filename]['rename_with'] = None        
    
    def add_item(self, mp3filename):
        """ 
        Append new MP3 file item with its tag to the 'mp3items' dict.
        Returns True if the file is correctly added, otherwise False 
        """
        
        is_added = 1
        try:
            if not self.mp3items.has_key(mp3filename):
                self.store_new_mp3(mp3filename)
                                                    
                APPLOG.info("New MP3 File loaded:")
                APPLOG.info(mp3filename)                
            else:
                APPLOG.warning("MP3 File already loaded:")
                APPLOG.warning(mp3filename)
                is_added = 2
        except:
            is_added = 0
            message_header = "Loading MP3 File: %s" % os.path.basename(mp3filename)
            APPLOG.exception(message_header)
            
        return is_added        

    def remove_item(self,mp3filename):
        """ Removes MP3 file items with 
        its tag from the 'mp3items' list """
        try:
            self.mp3items.pop(mp3filename)
            self.remove_for_update(mp3filename)
                
            APPLOG.info("Mp3 removed '%s'" % mp3filename)
        except KeyError:
            APPLOG.exception("Mp3 file is not loaded")
                
    def update(self, mp3):
        """ 
        Update the Mp3 tag.
        """
        try:
            metadata = self.get_metadata(mp3)
            tag = metadata.getTag()
            mp3_is_updated = tag.update()
            if mp3_is_updated:
                APPLOG.info("'%s' tag updated" % mp3)
            else:
                APPLOG.error("Error while updating '%s'" % mp3)
        except:
            APPLOG.exception("Cannot update '%s'" % mp3)
            mp3_is_updated = False
            
        return mp3_is_updated

    def rename(self,mp3):
        """        
        From a mp3 path check if the filename is changed then rename it.
        IMPORTANT: As the mp3 path is changed all the data assigned to
        this key has to be changed.        
        """
        try:
            mp3_final_filename = mp3
            rename_with = self.get_mp3_rename_with(mp3)
            if rename_with:
                mp3_dirname = os.path.dirname(mp3)
            	new_mp3 = os.path.join(mp3_dirname,rename_with) + '.mp3'
                
                if (mp3 != new_mp3):
                    if os.path.exists(mp3) and not os.path.exists(new_mp3):
                        os.rename(mp3,new_mp3)
                        self.set_mp3_rename_with(mp3,None)
                                        
                        # CRITICAL ACTION: Change the reference 
                        # to the old mp3 path
                        if self.change_mp3_reference(mp3,new_mp3):
                            mp3_final_filename = new_mp3
                                            
                        APPLOG.info("Mp3 renamed to '%s'" % new_mp3)
                    else:
                        mp3_final_filename = None
                else:
                    self.set_mp3_rename_with(mp3,None)
                    APPLOG.info("old Mp3 name = new Mp3 name. Rename do not apply")
        except:
            APPLOG.exception("Error while renaming '%s'" % mp3)
            mp3_final_filename = None
                   
        return mp3_final_filename

    ###########################################################################


    ###########################################################################
    ## Misc Methods

    def set_for_update(self,mp3filename):
        """
        Appends the mp3filename if it not exists on
        the update list
        """
        if mp3filename not in self.mp3toupdate:                
            self.mp3toupdate.append(mp3filename)

    def remove_for_update(self,mp3filename):
        """
        Removes the mp3filename if it exists on
        the update list
        """
        if mp3filename in self.mp3toupdate:                
            self.mp3toupdate.remove(mp3filename)        
            
    def is_any_pending_to_update(self):
        """ Returns True is the is some mp3 files
        pending to be updated """
        if len(self.mp3toupdate) > 0:            
            return True
        else:
            return False
    
    def pending_to_update(self, mp3):
        """ Returns True if the mp3 file given is in the list 
        of pendings to update """
        if mp3 in self.mp3toupdate:
            is_pending = True
        else:
            is_pending = False
        
        return is_pending
                
    def pending_files_to_update(self, mp3_list = []):
        """ Returns a list with the mp3 files that are
        pending to update and also exists in the list given """
        mapped_mp3_list = []
        for mp3_file_to_update in self.mp3toupdate:
            if mp3_file_to_update in mp3_list:
                mapped_mp3_list.append(mp3_file_to_update)
        
        return mapped_mp3_list       
    
    def change_mp3_reference(self,old_mp3,new_mp3):
        """ Change the key from 'mp3items' from 'mp3' to 'new_mp3' """        
        if self.mp3items.has_key(old_mp3):
            # Add new instance
            self.store_new_mp3(new_mp3)
            self.set_for_update(new_mp3)
            
            # Remove old instance
            self.remove_item(old_mp3)
                        
            ref_changed = True
            APPLOG.debug("Mp3 reference changed from")
            APPLOG.debug("%s to" % old_mp3)
            APPLOG.debug(new_mp3)
        else:
            ref_changed = False
            
        return ref_changed

    def get_metadata(self,mp3):
        """ Return the mp3 metadata if stored """
        metadata = None
        if self.mp3items.has_key(mp3):
            metadata = self.mp3items[mp3]['metadata']
        
        return metadata
        
    def get_apic_pixbuf(self,mp3):
        """ Return the mp3 apic pixbuf if stored """
        apic_pixbuf = None
        if self.mp3items.has_key(mp3):
            apic_pixbuf = self.mp3items[mp3]['apic_pixbuf']
        
        return apic_pixbuf
    
    def set_mp3_rename_with(self,mp3,new_mp3_filename):
        """
        Sets the new Mp3 filename to rename with        
        """
        if self.mp3items.has_key(mp3):
            self.mp3items[mp3]['rename_with'] = new_mp3_filename
                
    def get_mp3_rename_with(self,mp3):
        """ Return the mp3 new filename to rename with """
        rename_with = None
        if self.mp3items.has_key(mp3):
            rename_with = self.mp3items[mp3]['rename_with']
        
        return rename_with
                
    ###########################################################################


    ###########################################################################
    ## APIC Methods
    
    def get_apic_file_extension(self,mp3):
        """ Returns the mp3 apic mime type extension """
        try:
            # Get the actual Image Frames
            metadata = self.get_metadata(mp3)
            tag = metadata.getTag()
            apic_list = tag.getImages() 
            if len(apic_list) > 0:
               apic = apic_list[0]
               mime_type = apic.mimeType
               mime_extension = '.' + mime_type.split('/')[-1]                  
        except:
            APPLOG.exception("Error getting the mime type extension from %s" % mp3)        
            mime_extension = None       
        
        return mime_extension
    
    def export_apic_as(self,mp3,apic_path):
        """
        """
        try:
            path = os.path.dirname(apic_path)
            filename = os.path.basename(apic_path)
                
            # Get the actual Image Frames
            metadata = self.get_metadata(mp3)
            tag = metadata.getTag()
            apic_list = tag.getImages()
            if len(apic_list) > 0:
               apic = apic_list[0]
            
            apic.writeFile(path,filename)
        except:
            APPLOG.exception("Error writting out the APIC from %s" % mp3)
        
    def set_apic(self,mp3,apic):
        """
        Replace the first APIC that the mp3 metadata has. Always add the APIC
        with the First category OTHER(0) from the eyeD3 ImageFrame so this APIC
        will be the first to show in any external app
        """            
        try:
            # Low level on the APIC meter: OTHER = 0
            apic_type = eyeD3.ImageFrame.OTHER            
            
            # Get the actual Image Frames
            metadata = self.get_metadata(mp3)
            tag = metadata.getTag()
            mp3_apic_list = tag.getImages()
            
            # Remove all Image Frames from the mp3 and pop
            # the first image frame before extracted
            tag.removeImages()
            if len(mp3_apic_list) > 0: mp3_apic_list.pop(0)
            
            # Add the new Image Frame
            tag.addImage(apic_type,apic)
            
            # Append the old Image Frames to the mp3
            for mp3_apic in mp3_apic_list:
                tag.frames.append(mp3_apic)            
            
            # Sets the new APIC pixbuf
            self.set_apic_pixbuf(mp3,apic)
            
            # Finish the task
            apic_is_updated = True
            APPLOG.info("Mp3 APIC changed on %s" % mp3)
            
        except:
            APPLOG.exception("Cannot apply the new APIC on %s" % mp3)        
            apic_is_updated = False
            
        return apic_is_updated

    def set_apic_pixbuf(self,mp3,apic_filename):
        """ 
        Sets the mp3 apic pixbuf in the dictionary
        """
        apic_pixbuf = gtk.gdk.pixbuf_new_from_file_at_size(apic_filename,
                                                           env.APIC_WIDTH,
                                                           env.APIC_HEIGHT)        
        self.mp3items[mp3]['apic_pixbuf'] = apic_pixbuf        
                
    def extract_apic_pixbuf(self,mp3_metadata):
        """ 
        Extract and set a pixbuf from the metadata and
        return it
        """
        apic_pixbuf = None
        tag = mp3_metadata.getTag()
        apic_list = tag.getImages()
        if len(apic_list) > 0:
            apic = apic_list[0]
            apic_image_data = apic.imageData
                
            # Create a Pixbuf from the temporary image file
            temp_image_file = open(env.TEMP_APIC_PATH,'wb')
            temp_image_file.write(apic_image_data)
            temp_image_file.close()
                
            try:     
                apic_pixbuf = gtk.gdk.pixbuf_new_from_file_at_size(env.TEMP_APIC_PATH,
                                                                   env.APIC_WIDTH,
                                                                   env.APIC_HEIGHT)

            except:
                APPLOG.exception("Cannot load the APIC as a pixbuf")                                                              

        return apic_pixbuf                                                               
       
    def remove_apic(self,mp3):
        """
        Remove the first APIC that the mp3 metadata has.
        Then, if more apic exists, set the first one as the new APIC
        """            
        try:                  
            # Get the actual Image Frames
            metadata = self.get_metadata(mp3)
            tag = metadata.getTag()
            mp3_apic_list = tag.getImages()
            
            # Remove all Image Frames from the mp3 and pop
            # the first image frame before extracted
            tag.removeImages()
            if len(mp3_apic_list) > 0: mp3_apic_list.pop(0)
                        
            # Append the old Image Frames to the mp3
            for mp3_apic in mp3_apic_list:
                tag.frames.append(mp3_apic)            
            
            # Sets the new APIC pixbuf
            self.mp3items[mp3]['apic_pixbuf'] = self.extract_apic_pixbuf(metadata)
            
            # Finish the task
            apic_is_removed = True
            APPLOG.info("Mp3 APIC removed on %s" % mp3)
            
        except:
            APPLOG.exception("Cannot remove the APIC on %s" % mp3)        
            apic_is_removed = False
            
        return apic_is_removed

    ###########################################################################
