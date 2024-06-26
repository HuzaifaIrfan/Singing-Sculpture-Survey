
#################################################################################
####################  GUI Class #################################################
#################################################################################


import tkinter as tk
from tkinter import ttk
from tkinter.constants import *

from database import Database
from .admin_panel import Admin_Panel
from .user_panel import User_Panel

# from pathlib import Path

# # getting the name of the directory
# # where the this file is present.
# current = os.path.dirname(os.path.realpath(__file__))
  
# # Getting the parent directory name
# # where the current directory is present.
# parent = os.path.dirname(current)

import os
path = os.getcwd()
# print("Current directory", path)
# print()
# parent = os.path.dirname(path)
# print("Parent directory", parent)


ASSETS_PATH = os.path.abspath(os.path.join(path,'gui','assets'))


 

# ASSETS_PATH = Path(__file__).resolve().parent.parent / "assets"

# print(ASSETS_PATH)

###########################
# Main Tkinter Window
###########################


class GUI(tk.Tk):

    # BKGR_IMAGE_PATH = 'gui/img/survey_bg.png'

    def __init__(self, database_filename='db.sqlite3', *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.db = Database(database_filename)
        self.minsize(1200, 720)
        self.geometry("1200x720")

        logo = tk.PhotoImage(file=os.path.join(ASSETS_PATH, "iconbitmap.gif"))
        self.call('wm', 'iconphoto', self._w, logo)

        self.title("Singing Sculpture Survey")

        if self.db.get_settings('fullscreen') == '1':
            self.attributes('-fullscreen', True)
        else:
            pass
            # self.state('normal')

        self.tabControl = ttk.Notebook(self)
        User_Panel(self, self.tabControl, self.db)
        Admin_Panel(self, self.tabControl, self.db)
        self.tabControl.pack(expand=True, fill="both")

    def bring_to_front(self):
        self.lift()
        self.attributes('-topmost', True)

    def run_mainloop(self):
        self.bring_to_front()
        self.mainloop()
