
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

import subprocess
import requests
import zipfile
import os

from features.utilities import Utilities
from features.platform import Platform

import gi

gi.require_version("Adw", "1")

from gi.repository import Adw # type: ignore

class Terracles():
    def __init__(self):
        pass

    def play(self, play_button, notification_overlay):

        not_available_notification = Adw.Toast(title="Terraclès n'est pas encore disponible sur cette version du launcher !")
        notification_overlay.add_toast(not_available_notification)

        return

        self.install_tmodloader()

        import webbrowser
        webbrowser.open("steam://")

        import psutil
        import time

        def is_steam_running():
            for process in psutil.process_iter(['name']):
                if process.info['name'].lower() in ['steam', 'steam.exe']:
                    return True
            return False

        if is_steam_running():
            print("Steam est en cours d'exécution")
        else:
            print("Steam n'est pas en cours d'exécution")

        subprocess.run(["C:/Users/legdn/Documents/projets/oracles-project/oracles-launcher/testappdata/tmodloader/start-tModLoader.bat"], shell=True)

    def install_tmodloader(self):
        platform = Platform()
        platform.path()

        asset_name = "tModLoader.zip"
        tmodloader_zip_path = platform.terracles_directory + "/" + asset_name
        extract_path = platform.terracles_directory + "/tmodloader"

        os.makedirs(extract_path, exist_ok=True)

        if not os.path.exists(extract_path + "/start-tModLoader.bat"):
            print("...")
            url = "https://api.github.com/repos/tModLoader/tModLoader/releases/latest"
            response = requests.get(url)
            release_data = response.json()

            # Trouver l'asset souhaité
            for asset in release_data['assets']:
                if asset['name'] == asset_name:
                    download_url = asset['browser_download_url']
                    Utilities().copy_file(download_url, tmodloader_zip_path, "uri")
            
            os.makedirs(extract_path, exist_ok=True)

            with zipfile.ZipFile(tmodloader_zip_path, 'r') as zip_ref:
                zip_ref.extractall(extract_path)
        

