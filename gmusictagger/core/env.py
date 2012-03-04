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
import locale
import pygtk
pygtk.require('2.0')
import gtk


# To easy mark the traduction strings
import gettext
_ = gettext.gettext

# Locale Default
LOCALE_LANG, LOCALE_ENCODE = locale.getdefaultlocale()

# Program Constants
APP_NAME = "gmusictagger"
APP_VERSION = "2.2.1"

# Paths constants
PATH         = os.path.abspath(os.path.dirname(sys.argv[0]))
USER_PATH    = os.path.expanduser("~").decode(LOCALE_ENCODE)
CONFIG_PATH  = os.path.join(USER_PATH,".gmusictagger")
I18N_PATH    = "/usr/share/locale"
APPICON_PATH = "/usr/share/icons/hicolor/256x256/apps"
ICON_PATH    = os.path.join(PATH,"icons")
GLADE_PATH   = os.path.join(PATH,"ui","glade")

# Bind language on source files
gettext.textdomain(APP_NAME)
gettext.bindtextdomain(APP_NAME, I18N_PATH)

# Files constants
CONFIG_FILE = "gmusictagger.conf"
GLADE_MAIN = "gmusictagger.glade"
GLADE_SETTINGS = "settings.glade"
TEMP_APIC = ".temp_apic"
ICON_GMUSICTAGGER = os.path.join(APPICON_PATH,"gmusictagger.png")
ICON_EMPTY_APIC = os.path.join(ICON_PATH,"empty_apic.png")
ICON_ADD = os.path.join(ICON_PATH,"button_set/add_icon.png")
ICON_REMOVE = os.path.join(ICON_PATH,"button_set/remove_icon.png")
ICON_UPDATE = os.path.join(ICON_PATH,"button_set/update_icon.png")
ICON_FILL = os.path.join(ICON_PATH,"button_set/fill_icon.png")
ICON_PLAY = os.path.join(ICON_PATH,"button_set/play_icon.png")
ICON_SETTINGS = os.path.join(ICON_PATH,"button_set/settings_icon.png")
ICON_EXPORT_APIC = os.path.join(ICON_PATH,"button_set/export_icon.png")
ICON_REMOVE_APIC = os.path.join(ICON_PATH,"button_set/remove_icon.png")
ICON_ARROW_UP = os.path.join(ICON_PATH,"button_set/arrow_up_icon.png")
ICON_ARROW_DOWN = os.path.join(ICON_PATH,"button_set/arrow_down_icon.png")
ICON_EDITED_TRACK = os.path.join(ICON_PATH,"button_set/edited_track_icon.png")
ICON_GENERAL_SETTINGS = os.path.join(ICON_PATH,"button_set/general_settings_icon.png")
ICON_MUSIC_SETTINGS = os.path.join(ICON_PATH,"button_set/music_settings_icon.png")
ICON_APIC_SETTINGS = os.path.join(ICON_PATH,"button_set/apic_settings_icon.png")
ICON_DEFAULT_SETTINGS = os.path.join(ICON_PATH,"button_set/default_settings_icon.png")

# Icons and Images
APIC_HEIGHT = 160
APIC_WIDTH = 160
TEMP_APIC_PATH = os.path.join(CONFIG_PATH,TEMP_APIC)

GMUSICTAGGER_BUF = gtk.gdk.pixbuf_new_from_file(ICON_GMUSICTAGGER)
EMPTY_APIC_BUF160 = gtk.gdk.pixbuf_new_from_file_at_size(ICON_EMPTY_APIC,160,160)
ADD_BUF32 = gtk.gdk.pixbuf_new_from_file_at_size(ICON_ADD,32,32)
REMOVE_BUF32 = gtk.gdk.pixbuf_new_from_file_at_size(ICON_REMOVE,32,32)
UPDATE_BUF32 = gtk.gdk.pixbuf_new_from_file_at_size(ICON_UPDATE,32,32)
FILL_BUF32 = gtk.gdk.pixbuf_new_from_file_at_size(ICON_FILL,32,32)
PLAY_BUF16 = gtk.gdk.pixbuf_new_from_file_at_size(ICON_PLAY,16,16)
PLAY_BUF32 = gtk.gdk.pixbuf_new_from_file_at_size(ICON_PLAY,32,32)
SETTINGS_BUF32 = gtk.gdk.pixbuf_new_from_file_at_size(ICON_SETTINGS,32,32)
EXPORT_APIC_BUF16 = gtk.gdk.pixbuf_new_from_file_at_size(ICON_EXPORT_APIC,16,16)
REMOVE_APIC_BUF16 = gtk.gdk.pixbuf_new_from_file_at_size(ICON_REMOVE_APIC,16,16)
ARROW_UP_BUF16 = gtk.gdk.pixbuf_new_from_file_at_size(ICON_ARROW_UP,16,16)
ARROW_DOWN_BUF16 = gtk.gdk.pixbuf_new_from_file_at_size(ICON_ARROW_DOWN,16,16)
EDITED_TRACK_BUF24 = gtk.gdk.pixbuf_new_from_file_at_size(ICON_EDITED_TRACK,24,24)
GENERAL_SETTINGS_BUF32 = gtk.gdk.pixbuf_new_from_file_at_size(ICON_GENERAL_SETTINGS,32,32)
MUSIC_SETTINGS_BUF32 = gtk.gdk.pixbuf_new_from_file_at_size(ICON_MUSIC_SETTINGS,32,32)
APIC_SETTINGS_BUF32 = gtk.gdk.pixbuf_new_from_file_at_size(ICON_APIC_SETTINGS,32,32)
DEFAULT_SETTINGS_BUF16 = gtk.gdk.pixbuf_new_from_file_at_size(ICON_DEFAULT_SETTINGS,16,16)


## Mp3Tree Columns Configuration
COLUMN_IDS = ["FILE","TRCK","TIT2","TPE1","TPE2",
              "TPE3","TPE4","TCOM","TALB","TYER",
              "TCON","COMM","TIME","BITRATE","PATH"]
MP3FRAME_PATTERN = {'%trck': 'TRCK', '%title': 'TIT2',
                    '%artist': 'TPE1', '%album': 'TALB'}                   
COLUMN_ID_INDEX = {'SELEC': 0, 'FILE': 1, 'TRCK': 2, 'TIT2': 3,
                   'TPE1': 4, 'TPE2': 5, 'TPE3': 6, 'TPE4': 7,
                   'TCOM': 8, 'TALB': 9, 'TYER': 10, 'TCON': 11,
                   'COMM': 12, 'TIME': 13, 'BITRATE': 14, 'PATH': 15}
MODEL_ID_INDEX = {'SELEC': 0, 'FILE': 1, 'TRCK': 2, 'TIT2': 3,
                   'TPE1': 4, 'TPE2': 5, 'TPE3': 6, 'TPE4': 7,
                   'TCOM': 8, 'TALB': 9, 'TYER': 10, 'TCON': 11,
                   'COMM': 13, 'TIME': 14, 'BITRATE': 15, 'PATH': 16}
MP3TREE_COLUMNS = [{'col_id': 'SELEC',
                    'index': MODEL_ID_INDEX['SELEC'],
                    'type': bool,
                    'name': _("Sel.")},
                   {'col_id': 'FILE',
                     'index': MODEL_ID_INDEX['FILE'],
                     'type': str,
                     'name': _("Filename")},
                   {'col_id': 'TRCK',
                    'index': MODEL_ID_INDEX['TRCK'],
                    'type': str,
                    'name': _("#")},
                   {'col_id': 'TIT2',
                    'index': MODEL_ID_INDEX['TIT2'],
                    'type': str,
                    'name': _("Title")},
                   {'col_id': 'TPE1',
                    'index': MODEL_ID_INDEX['TPE1'],
                    'type': str,
                    'name': _("Artist")},
                   {'col_id': 'TPE2',
                    'index': MODEL_ID_INDEX['TPE2'],
                    'type': str,
                    'name': _("Band")},
                   {'col_id': 'TPE3',
                    'index': MODEL_ID_INDEX['TPE3'],
                    'type': str,
                    'name': _("Performer")},
                   {'col_id': 'TPE4',
                    'index': MODEL_ID_INDEX['TPE4'],
                    'type': str,
                    'name': _("Remix")},
                   {'col_id': 'TCOM',
                    'index': MODEL_ID_INDEX['TCOM'],
                    'type': str,
                    'name': _("Composer")},
                   {'col_id': 'TALB',
                    'index': MODEL_ID_INDEX['TALB'],
                    'type': str,
                    'name': _("Album")},
                   {'col_id': 'TYER',
                    'index': MODEL_ID_INDEX['TYER'],
                    'type': str,
                    'name': _("Year")},
                   {'col_id': 'TCON',
                    'index': MODEL_ID_INDEX['TCON'],
                    'type': object,
                    'name': _("Genre")},
                   {'col_id': 'COMM',
                    'index': MODEL_ID_INDEX['COMM'],
                    'type': str,
                    'name': _("Comments")},
                   {'col_id': 'TIME',
                    'index': MODEL_ID_INDEX['TIME'],
                    'type': str,
                    'name': _("Duration")},
                   {'col_id': 'BITRATE',
                    'index': MODEL_ID_INDEX['BITRATE'],
                    'type': str,
                    'name': _("Quality")},
                   {'col_id': 'PATH',
                    'index': MODEL_ID_INDEX['PATH'],
                    'type': str,
                    'name': _("Path")}
                  ]

# Config file Constants
HEADER = """# GMusicTagger config file.
# Do not edit this file! Use the GUI preferences instead.

"""   

# Default preferences and properties
DEFAULTS = {"LOG": {"name": "gmusictagger.log",
                    "path": os.path.join(USER_PATH,".gmusictagger"),
                    "mode": 'w',
                    "datetime": '%d/%m/%Y %H:%M:%S',
                    "format": '%(asctime)s :: %(name)18s[%(levelname)8s]: %(message)s',
                    "level": 20},
            "MUSIC": {"start-folder": USER_PATH,
                      "player": '/usr/bin/env totem'},
            "COVER": {"start-folder": USER_PATH},
            "COLUMNS": {"FILE": {"visible": True,
                                 "editable": True,
                                 "background": '#00008800bbff',
                                 "foreground": '#000000000000'},
                        "TRCK": {"visible": True,
                                 "editable": True,
                                 "background": '#ffffffffffff',
                                 "foreground": '#000000000000'},
                        "TIT2": {"visible": True,
                                 "editable": True,
                                 "background": '#ffffffffffff',
                                 "foreground": '#000000000000'},
                        "TPE1": {"visible": True,
                                 "editable": True,
                                 "background": '#ffffffffffff',
                                 "foreground": '#000000000000'},
                        "TPE2": {"visible": False,
                                 "editable": True,
                                 "background": '#ffffffffffff',
                                 "foreground": '#000000000000'},
                        "TPE3": {"visible": False,
                                 "editable": True,
                                 "background": '#ffffffffffff',
                                 "foreground": '#000000000000'},                                 
                        "TPE4": {"visible": False,
                                 "editable": True,
                                 "background": '#ffffffffffff',
                                 "foreground": '#000000000000'},
                        "TCOM": {"visible": False,
                                 "editable": True,
                                 "background": '#ffffffffffff',
                                 "foreground": '#000000000000'},
                        "TALB": {"visible": True,
                                 "editable": True,
                                 "background": '#ffffffffffff',
                                 "foreground": '#000000000000'},
                        "TYER": {"visible": True,
                                 "editable": True,
                                 "background": '#ffffffffffff',
                                 "foreground": '#000000000000'},
                        "TCON": {"visible": True,
                                 "editable": True,
                                 "background": '#ffffffffffff',
                                 "foreground": '#000000000000'},
                        "COMM": {"visible": True,
                                 "editable": True,
                                 "background": '#ffffffffffff',
                                 "foreground": '#000000000000'},
                        "TIME": {"visible": True,
                                 "editable": False,
                                 "background": '#00008800bbff',
                                 "foreground": '#000000000000'},
                        "BITRATE": {"visible": True,
                                   "editable": False,
                                   "background": '#00008800bbff',
                                   "foreground": '#000000000000'},
                        "PATH": {"visible": False,
                                 "editable": False,
                                 "background": '#ffffffffffff',
                                 "foreground": '#000000000000'},
                       }
           }
           
# Not allowed characters on filenames (Windows/Mac OsX/Linux)
INVALID_FILENAME_CHARS = ['\\','/',':','*','?','"','<','>','|']


