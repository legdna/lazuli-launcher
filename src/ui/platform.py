import platform
import gi
import ui.about as about

gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")
gi.require_version("GLib", "2.0")

from gi.repository import Gtk, GLib, Adw

class Platform():
    def __init__(self):
        self.pf = platform.system()

        if self.pf != 'Linux':
            GLib.setenv("GTK_CSD", "0", False)
            self.appwindow = Gtk.ApplicationWindow
        else:
            self.appwindow = Adw.ApplicationWindow

    def windows_theme(self, window, title):
        if self.pf == 'Windows':
            from ctypes import windll
            import pywinstyles

            hwnd = windll.user32.FindWindowW(None, title)
            pywinstyles.apply_style(hwnd, style="mica")
        else:
            pass

    def apparence(self, window):
        if self.pf != 'Linux':
            window.set_child(window.overlaysw)
        else:
            window.headerbar = Adw.HeaderBar(
                css_classes=[
                    "flat"
                ]
            )

            window.box.append(window.headerbar)
            window.set_content(window.overlaysw)
    
    def about(self, window):
        if self.pf != 'Linux':
            about.NativeAboutDialog(window, self.windows_theme)
        else:
            about.AdwAboutDialog(window)
        
    def path(self):
        if self.pf == 'Windows':
            self.appdata = "./testappdata"
        elif self.pf == 'Darwin':
            appdata = ""
        else:
            appdata = ""