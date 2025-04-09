
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

from pathlib import Path
import json

from features.platform import Platform

import gi

gi.require_version("Gio", "2.0")
gi.require_version("GLib", "2.0")

from gi.repository import Gio, GLib # type: ignore

class Utilities():
    def __init__(self):
        pass

    def copy_file(self, src_path, dest_path, src_type, callback=None):
        def on_copy_finished(source_file, result):
            try:
                success = source_file.copy_finish(result)
                print("File copy finished:", "Success" if success else "Failed")
            except GLib.Error as e:
                print("Error during file copy:", e.message)
        
        if callback == None:
            callback = on_copy_finished

        if src_type == "uri":
            file = Gio.File.new_for_uri(src_path)
        elif src_type == "path":
            file = Gio.File.new_for_path(src_path)
        else:
            print("Error : " + src_type + " dosn't exist !")
            return

        #cancellable = Gio.Cancellable()

        file.copy_async(
            Gio.File.new_for_path(dest_path),
            Gio.FileCopyFlags.OVERWRITE,
            GLib.PRIORITY_DEFAULT,
            None,
            None,
            callback
        )

    def load_profile(self):
        platform = Platform()

        if Path(platform.auth_file_path).is_file():
            with open(platform.auth_file_path) as auth_file:
                self.login_data = json.load(auth_file)
                print("Les identifiants de connexion ont été importés avec succès !")
                print(self.login_data)