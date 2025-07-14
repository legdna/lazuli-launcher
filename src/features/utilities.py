
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

from pathlib import Path
import json
import os
import psutil
import requests

from features.platform import Platform

import gi

gi.require_version("Gio", "2.0")
gi.require_version("GLib", "2.0")

from gi.repository import Gio, GLib # type: ignore

platform = Platform()

def download_file(src_path, dest_path, callback):
        
    #if callback == None:
    #    callback = on_copy_finished

    #if src_type == "uri":
    #    file = Gio.File.new_for_uri(src_path)
    #elif src_type == "path":
    #    file = Gio.File.new_for_path(src_path)
    #else:
    #    print(f"Error : {src_type} dosn't exist !")
    #    return

    #def on_ready(file, result, user_data):
    #    success, content, etag = file.load_contents_finish(result)
    #    if success:
    #        with open(dest_path, "wb") as f:
    #            f.write(content)
    #           
    #        print("Téléchargement terminé")
    #
    #        if callback:
    #            callback(file, True)
    #    else:
    #        print("Erreur lors du téléchargement")
    #
    #        if callback:
    #            callback(file, False)
    #
    #file.load_contents_async(None, on_ready, None)
    
    def get_file(task, object, any, cancellable):

        try:
            file = requests.get(src_path, stream=True)
            file.raise_for_status()
            with open(dest_path, "wb") as f:
                for chunk in file.iter_content(4096):
                    f.write(chunk)
        except Exception as e:
            task.return_boolean(False)
            return

        task.return_boolean(True)

    get_file_task = Gio.Task.new(None, None, callback, None)
    get_file_task.run_in_thread(get_file)

def is_process_running():
    LAUNCHER_CONFIG = json.loads(Gio.resources_lookup_data("/xyz/oraclesmc/OraclesLauncher/config.json", Gio.ResourceLookupFlags.NONE).get_data().decode())

    if os.path.exists(platform.oracles_lockfile):
        with open(platform.oracles_lockfile) as f:
            oracles_pid = int(f.read())
        
        if psutil.pid_exists(oracles_pid):
            try:
                for arg in psutil.Process(oracles_pid).cmdline():
                    if arg == f'-Dminecraft.launcher.brand={LAUNCHER_CONFIG["launcher"]["NAME"]}':
                        #is_running_notification = Adw.Toast(title="Oraclès est déjà en cours d'éxecution !")
                        #notification_overlay.add_toast(is_running_notification)
                        return True
            except:
                os.remove(platform.oracles_lockfile)
    
    return False

def get_pid():
    if os.path.exists(platform.oracles_lockfile):
        with open(platform.oracles_lockfile) as f:
            pid = int(f.read())
            
            return pid
