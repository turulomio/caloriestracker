## @namespace caloriestracker.shortcuts
## @brief Creates windows shortcuts

import os
import pythoncom #Viene en pywin32
import pkg_resources
from win32com.shell import shell, shellcon

def create():
    shortcut = pythoncom.CoCreateInstance (
      shell.CLSID_ShellLink,
      None,
      pythoncom.CLSCTX_INPROC_SERVER,
      shell.IID_IShellLink
    )

    icon=pkg_resources.resource_filename("caloriestracker","images/caloriestracker.ico")
    shortcut.SetPath (r'caloriestracker.exe')
    shortcut.SetDescription ("Calories tracker system")
    shortcut.SetIconLocation (icon, 0)
     
    desktop_path = shell.SHGetFolderPath (0, shellcon.CSIDL_DESKTOP, 0, 0)
    persist_file = shortcut.QueryInterface (pythoncom.IID_IPersistFile)
    persist_file.Save (os.path.join (desktop_path, "caloriestracker.lnk"), 0)
    print("A shortcut have been placed in your desktop ;)")    
    
    shortcut = pythoncom.CoCreateInstance (
      shell.CLSID_ShellLink,
      None,
      pythoncom.CLSCTX_INPROC_SERVER,
      shell.IID_IShellLink
    )

    icon=pkg_resources.resource_filename("caloriestracker","images/caloriestracker.ico")
    shortcut.SetPath (r'caloriestracker_init.exe')
    shortcut.SetDescription ("Calories tracker system database initialization")
    shortcut.SetIconLocation (icon, 0)
     
    desktop_path = shell.SHGetFolderPath (0, shellcon.CSIDL_DESKTOP, 0, 0)
    persist_file = shortcut.QueryInterface (pythoncom.IID_IPersistFile)
    persist_file.Save (os.path.join (desktop_path, "caloriestracker_init.lnk"), 0)
    print("A shortcut have been placed in your desktop ;)")


def remove():
    desktop_path = shell.SHGetFolderPath (0, shellcon.CSIDL_DESKTOP, 0, 0)
    os.remove(os.path.join (desktop_path, "caloriestracker.lnk"))
    os.remove(os.path.join (desktop_path, "caloriestracker_init.lnk"))

