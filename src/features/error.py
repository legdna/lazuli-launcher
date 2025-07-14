
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

import gi

gi.require_version("Gtk", "4.0")

from gi.repository import Gtk # type: ignore

class ErrorWindow(Gtk.Window):
    def __init__(self, error_title):
        super.__init__()

        self.main_box = Gtk.Box(
            orientation=Gtk.Orientation.VERTICAL,
            valign=Gtk.Align.CENTER
        )
        self.set_child(self.main_box)

        self.error_box = Gtk.Box(
            orientation=Gtk.Orientation.HORIZONTAL,
            hexpand=True
        )
        self.main_box.append(self.error_box)

        self.error_icon = Gtk.Image(
            
        )
        self.error_box.append(self.error_icon)

        self.error_title = Gtk.Label(
            label=error_title
        )
        self.error_box.append(self.error_title)