
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

import gi

gi.require_version("Gtk", "4.0")
gi.require_version("Gdk", "4.0")
gi.require_version("Adw", "1")

from gi.repository import Gtk, Adw, Gdk # type: ignore

class NativeAboutDialog(Gtk.Window):
    def __init__(self, parent, action, windows_theme, update_methode):
        super().__init__()

        # Configure le dialogue
        self.set_transient_for(parent)
        title = "À propos"
        self.set_title(title)
        self.set_modal(True)
        self.set_default_size(300, 150)

        # Ajouter des widgets personnalisés
        vbox = Gtk.Box(
            orientation=Gtk.Orientation.VERTICAL,
            valign=Gtk.Align.CENTER,
            spacing=10
        )
        vbox.set_margin_top(45)
        vbox.set_margin_bottom(50)
        vbox.set_margin_start(50)
        vbox.set_margin_end(50)

        application_icon = Gtk.Image(
            icon_name="oracles",
            pixel_size=120
        )
        vbox.append(application_icon)

        application_name = Gtk.Label(
            label="Oraclès Launcher",
            css_classes=[
                "title-1"
            ]
        )
        vbox.append(application_name)

        version = Gtk.Button(
            label="2.0.0",
            hexpand=False,
            css_classes=[
                "title-2",
                "suggested-action",
                "pill",
                "flat"
            ]
        )
        version.connect("clicked", self.on_version_clicked)
        vbox.append(version)

        self.set_child(vbox)

        self.connect("realize", lambda widget: windows_theme(self, title))
        self.show()
    
    def on_version_clicked(self, button):
        clipboard = Gdk.Display.get_default().get_clipboard()
        clipboard.set("2.0.0")

class AdwAboutDialog():
    def __init__(self, parent):
        parent.about = Adw.AboutDialog(
            application_icon="data/oracles-logo2.png",
            application_name="Oraclès Launcher",
            version="2.0.0",

            website="https://oraclesmc.xyz",
            developers=[
                "legdna"
            ]
        )
        parent.about.present(parent)
        