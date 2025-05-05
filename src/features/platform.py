
# Oraclès Launcher
# ---
# Copyright (C) 2025 - legdna <legdna@proton.me>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License version 3 for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

import platform
import gi
import os
import sys
import darkdetect

gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")
gi.require_version("GLib", "2.0")

from gi.repository import Gtk, GLib, Adw # type: ignore

class Platform():
    def __init__(self):
        self.pf = platform.system()

        self.path()

        if self.pf != 'Linux':
            GLib.setenv("GTK_CSD", "0", False)
            self.appwindow = Gtk.ApplicationWindow
            self.native_window = Gtk.Window
        else:
            self.appwindow = Adw.ApplicationWindow
            self.native_window = Adw.Dialog

        match self.pf:
            case "Windows":
                self.os_release = "windows"
            case "Linux":
                self.os_release = "linux"
            case "Darwin":
                self.os_release = "mac"

    def windows_theme(self, window, title):
        def system_theme_color():
            nonlocal hwnd

            if darkdetect.isDark():
                pywinstyles.apply_style(hwnd, style="mica")
            else:
                pywinstyles.apply_style(hwnd, style="normal")
            
            #return GLib.SOURCE_CONTINUE

        if self.pf == 'Windows':
            from ctypes import windll
            import pywinstyles

            hwnd = windll.user32.FindWindowW(None, title)
            #pywinstyles.apply_style(hwnd, style="mica")

            system_theme_color()
            #GLib.timeout_add_seconds(1, system_theme_color)

    def apparence(self, window, widget=None):
        if self.pf != 'Linux' and widget == None:
            window.set_child(window.main_window_box)
        elif widget == None:
            window.headerbar = Adw.HeaderBar(
                css_classes=[
                    "flat"
                ]
            )

            window.main_window_box.append(window.headerbar)
            window.set_content(window.main_window_box)
        elif self.pf != 'Linux':
            window.set_child(widget)
        else:
            window.headerbar = Adw.HeaderBar(
                css_classes=[
                    "flat"
                ]
            )

            widget.append(window.headerbar)
            window.set_child(widget)
    
    def dialog(self, window, native_dialog, adw_dialog, action, update_methode=None):
        #if self.pf != 'Linux':
        native_dialog(window, action, self.windows_theme, update_methode)
        #else:
        #    adw_dialog(window)

    def path(self):
        if self.pf == 'Windows':
            self.launcher_directory = os.getenv('APPDATA') + "/OraclesLauncher"
            self.temp_directory = os.getenv('TEMP')

        elif self.pf == 'Darwin':
            self.launcher_directory = ""
        elif self.pf == 'Linux':
            self.launcher_directory = os.getenv('HOME') + "/.var/app/xyz.oraclesmc.OraclesLauncher"
        else:
            sys.exit("Error : Platform unsupported !")

        self.oracles_directory = f"{self.launcher_directory}/oracles"
        self.oracles_lockfile = f"{self.oracles_directory}/oracles.lockfile"

        self.terracles_directory = f"{self.launcher_directory}/terracles"
        self.profiles_directory = f"{self.launcher_directory}/profiles"

        self.auth_file_path = f"{self.profiles_directory}/auth.json"

        self.default_profile_image = "data/default_profile_logo.png"