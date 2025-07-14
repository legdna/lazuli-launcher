
# Lazuli Launcher
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

import json
import gi

gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")
gi.require_version("Gio", "2.0")

from gi.repository import Gtk, Adw, Gio # type: ignore

class Home():
    def __init__(self, main_window):
        data = Gio.resources_lookup_data("/xyz/oraclesmc/OraclesLauncher/config.json", Gio.ResourceLookupFlags.NONE)
        config = json.loads(data.get_data().decode())

        self.launcher_version = Gtk.Button(
            label=f"{config["launcher"]["RELEASE_TYPE"]} - {config["launcher"]["VERSION"]}",
            hexpand=False,
            halign=Gtk.Align.CENTER,
            margin_top=20,
            css_classes=[
                "title-2",
                "alpha-version",
            ]
        )
        main_window.center_main_menu_box.append(self.launcher_version)