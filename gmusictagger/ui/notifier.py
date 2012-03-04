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

import core.env as env
from core.env import _
import ui.message as message

def show_notification(title,message): print "%s -> %s" % (title,message)

try:
    import pynotify

    if pynotify.init(env.APP_NAME):
        def show_notification(title,message):
            notification = pynotify.Notification(title, message)
            notification.set_icon_from_pixbuf(env.GMUSICTAGGER_BUF)
            notification.set_urgency(pynotify.URGENCY_LOW)
            notification.show()
except ImportError:
    error_title = _("GMusicTagger: Notifier module")
    error_message = _("Cannot start notification module.\n") + \
                    _("Try installing 'python-notify' package")
    message.error(error_title, error_message)
                  
