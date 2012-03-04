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
import traceback

import pygtk
pygtk.require('2.0')
import gtk


def info(title="Information",message="This is an information dialog",parent=None):
    dialog = gtk.MessageDialog(parent,
                               gtk.DIALOG_MODAL|gtk.DIALOG_DESTROY_WITH_PARENT,
                               gtk.MESSAGE_INFO,
                               gtk.BUTTONS_OK)
    dialog.set_markup(message)
    dialog.set_title(title)
    response = dialog.run()    
    if response == gtk.RESPONSE_OK:
        ret = True
    elif response == gtk.RESPONSE_DELETE_EVENT:
        ret = False    
    
    dialog.destroy()
    return ret
    
def question(title="Question",message="Would you accept this terms?",parent=None):
    dialog = gtk.MessageDialog(parent,
                               gtk.DIALOG_MODAL|gtk.DIALOG_DESTROY_WITH_PARENT,
                               gtk.MESSAGE_QUESTION,
                               gtk.BUTTONS_YES_NO)
    dialog.set_markup(message)      
    dialog.set_title(title)
    response = dialog.run()
    if response == gtk.RESPONSE_YES:
        ret = True
    elif response == gtk.RESPONSE_NO:
        ret = False
    elif response == gtk.RESPONSE_DELETE_EVENT:
        ret = False
        
    dialog.destroy()
    return ret        
    
def warning(title="Warning",message="Something unexpected ocurred",parent=None):
    dialog = gtk.MessageDialog(parent,
                               gtk.DIALOG_MODAL|gtk.DIALOG_DESTROY_WITH_PARENT,
                               gtk.MESSAGE_WARNING,
                               gtk.BUTTONS_OK)
    dialog.set_markup(message)
    dialog.set_title(title)
    response = dialog.run()    
    if response == gtk.RESPONSE_OK:
        ret = True
    elif response == gtk.RESPONSE_DELETE_EVENT:
        ret = False    
    
    dialog.destroy()
    return ret
    
def error(title="Error",message="An error has ocurred!",parent=None):
    dialog = gtk.MessageDialog(parent,
                               gtk.DIALOG_MODAL|gtk.DIALOG_DESTROY_WITH_PARENT,
                               gtk.MESSAGE_ERROR,
                               gtk.BUTTONS_OK)
                               
    dialog.set_markup(message)
    dialog.set_title(title)
    response = dialog.run()    
    if response == gtk.RESPONSE_OK:
        ret = True
    elif response == gtk.RESPONSE_DELETE_EVENT:
        ret = False    
    
    dialog.destroy()
    return ret

def exception(title="Exception",message="An exception has ocurred...",parent=None):    
    dialog = gtk.MessageDialog(parent,
                               gtk.DIALOG_MODAL|gtk.DIALOG_DESTROY_WITH_PARENT,
                               gtk.MESSAGE_ERROR,
                               gtk.BUTTONS_OK)
                               
    dialog.set_title(title)
    dialog.set_markup(message)
    exception_message = traceback.format_exc()
    if exception_message.isalpha():
        dialog.format_secondary_text(exception_message)
        
    
    response = dialog.run()    
    if response == gtk.RESPONSE_OK:
        ret = True
    elif response == gtk.RESPONSE_DELETE_EVENT:
        ret = False    
    
    dialog.destroy()
    return ret


