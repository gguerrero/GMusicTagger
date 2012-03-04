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

import pango

import pygtk
pygtk.require('2.0')
import gtk

from core.env import _

class ProgressBar(gtk.ProgressBar):
    """
    A Gtk ProgressBar derived class with some 
    extra methods to make easy the control.
    """
    
    fraction_increment = 0.0
    actual_fraction = 0.0
    
    def __init__(self):
        """ """
        gtk.ProgressBar.__init__(self)      

    def set_fraction_increment(self,total):
        """ 
        Reset and calculate the progressbar values
        """
        self.actual_fraction = 0.0
        self.fraction_increment = (100.0 / total) / 100.0         
              
        
    def next_fraction(self):
        """ 
        Refresh the progressbar fraction setting
        the new fraction value of the sequence
        """
        text = "%d%s" % (round(self.actual_fraction*100),
                         _("% Complete"))
        self.set_text(text)
        self.set_fraction(self.actual_fraction)        
        
        self.actual_fraction += self.fraction_increment
        if self.actual_fraction > 1.0: self.actual_fraction = 1.0
    
        while gtk.events_pending(): gtk.main_iteration()
        
    def cancel_message(self):
        """
        Shows a cancel message and the progressbar at 100%
        """
        self.set_fraction(1.0)
        self.set_text(_("Action cancelled..."))
        while gtk.events_pending(): gtk.main_iteration()
        

class ProgressBarBox(gtk.VBox):
    """
    Build a gtk visual box composed of a
    label, a progressbar and a cancel button.
    This box help to show and cancel any events
    that your application could perform.
    """
    
    # Cancel action control
    cancel_action = False
    
    def __init__(self):
        """
        """
        # VBox initialize
        gtk.VBox.__init__(self)
        
        # Utility widgets
        self.progressbar = ProgressBar()
        self.label = gtk.Label()
        self.label.set_ellipsize(pango.ELLIPSIZE_END)
        self.cancel_button = gtk.Button()
        self.cancel_button.set_relief(gtk.RELIEF_NONE)
        self.cancel_button.set_tooltip_text(_("Cancel this action"))
        stock_cancel_image = gtk.Image()
        stock_cancel_image.set_from_stock(gtk.STOCK_CANCEL,gtk.ICON_SIZE_BUTTON)
        self.cancel_button.set_image(stock_cancel_image)
        self.cancel_button.connect("clicked",self.__on_cancel_button_clicked)
        
        # Horizontal Container
        self.hbox = gtk.HBox()      
        self.hbox.pack_start(self.progressbar,expand=True,fill=True)
        self.hbox.pack_start(self.cancel_button,expand=False,fill=False,padding=5)
        
        # Pack all the widgets
        self.pack_start(self.label,expand=False,fill=False,padding=10)
        self.pack_start(self.hbox,expand=False,fill=False)
        
        # Perform a show on all widget and hide them
        self.show_all()
        self.hide()
    
    def __on_cancel_button_clicked(self,button):
        """
        Sets the progress action to cancelled so other external GUI could execute the cancel process
        """
        self.cancel_action = True
    
    def cancel_message(self, text=None):
        """
        """
        if text != None:
            self.set_label_text(text)
        self.progressbar.cancel_message()
    
    def set_label_text(self,text):
        """
        """
        self.label.set_text(text)
        
    def set_new_bar(self,total):
        """
        """
        self.cancel_action = False
        self.progressbar.set_fraction_increment(total)
        
    def next(self,text=None):
        """
        """
        if text != None:
            self.set_label_text(text)
        self.progressbar.next_fraction()
        
                
    
