
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
import os

from features.platform import Platform

import gi

gi.require_version("Gio", "2.0")

from gi.repository import Gio # type: ignore

platform = Platform()
LAUNCHER_CONFIG = json.loads(Gio.resources_lookup_data("/xyz/oraclesmc/OraclesLauncher/config.json", Gio.ResourceLookupFlags.NONE).get_data().decode())

def init_settings():
    if os.path.isfile(f"{platform.launcher_directory}/settings.json"):
        return
    
    settings_data = {"version": "1", "launcher": {"installed_version": LAUNCHER_CONFIG["launcher"]["VERSION"]}, "oracles": {"installed_version": [], "selected_version": ""}}

    with open(platform.settings_file_path, 'w') as settings_file:
        json.dump(settings_data, settings_file, indent=4)
        print("Les paramètres on été enregistrés avec succès !")

def get_settings():
    settings_data = json.loads(platform.settings_file_path)
    return settings_data