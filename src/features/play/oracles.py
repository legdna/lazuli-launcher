
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

import os
import shutil
import minecraft_launcher_lib
import json
from zipfile import ZipFile
import subprocess

import features.auth
from features.platform import Platform
from features.utilities import Utilities

import gi

gi.require_version("Gio", "2.0")
gi.require_version("GLib", "2.0")
gi.require_version("Soup", "3.0")

from gi.repository import GLib, Gio, Soup # type: ignore

platform = Platform()
utilities = Utilities()

profile_data = None
play_button = None
progressbar = None

def oracles(button, progress, show_profile_menu):
    global profile_data, play_button, progressbar

    #progressbar.add_css_class("title-2")

    profile_data = features.auth.load_file()
    play_button = button
    progressbar = progress

    if profile_data == None:
        show_profile_menu()
        return
    
    play_button.set_visible(False)
    progressbar.set_visible(True)
    progressbar.set_show_text(True)
    progressbar.set_text("Récupération des identifiants de connexion")

    GLib.timeout_add(100, lambda widget: on_timeout(progressbar), GLib.PRIORITY_DEFAULT)

    launch_minecraft_task = Gio.Task.new()
    launch_minecraft_task.run_in_thread(launch_minecraft)

def launch_minecraft(task, object, any, cancellable):
    global profile_data, play_button, progressbar
    print(profile_data)

    gresource_data = Gio.resources_lookup_data("/xyz/oraclesmc/OraclesLauncher/config.json", Gio.ResourceLookupFlags.NONE)
    config = json.loads(gresource_data.get_data().decode())
    CLIENT_ID = config["microsoft"]["CLIENT_ID"]
    REDIRECT_URL = config["microsoft"]["REDIRECT_URL"]

    soup_session = Soup.Session()

    try:
        #refresh token
        profile_data = minecraft_launcher_lib.microsoft_account.complete_refresh(CLIENT_ID, None, REDIRECT_URL, profile_data["refresh_token"])
        features.auth.update_profile(profile_data["id"], profile_data)
    except:
        play_button.set_visible(True)
        print("Erreur lors du renouvellement du profile utilisateur !")
        return
        
    try:
        update_url = "https://oraclesmc.xyz/update.json"

        get_latest_update_file = Soup.Message.new("GET", update_url)
        latest_update_file = soup_session.send_and_read(get_latest_update_file).get_data().decode()

        update_data = json.loads(latest_update_file)
    except:
        play_button.set_visible(True)
        return

    oracles_version = "1"
    loader_version = "0.16.0"
    minecraft_version = "1.21"
    modpack_version = update_data["modpack"]["version"]
    java_version = "21"
    fabric_loader_version = f"fabric-loader-{loader_version}-{minecraft_version}"

    modpack_download_link = update_data["modpack"]["url"]

    oracles_version_directory = f"{platform.oracles_directory}/v{oracles_version}"
    minecraft_directory = f"{oracles_version_directory}/.minecraft"
    java_directory = f"{oracles_version_directory}/java"

    progressbar.set_text(f"Récupération de la version {java_version} de java")

    # Création du répertoire java
    os.makedirs(java_directory, exist_ok=True)
    java_zip_path = f"{java_directory}/java-{java_version}-jre.zip"
    java_version_directory = f"{java_directory}/{java_version}"

    # Obtention de la dernière version de java
    latest_java_url = f"https://api.adoptium.net/v3/assets/latest/{java_version}/hotspot?architecture=x64&image_type=jre&os=windows&vendor=eclipse"
    get_latest_java = Soup.Message.new("GET", latest_java_url)
    latest_java = soup_session.send_and_read(get_latest_java).get_data().decode()
    latest_java = json.loads(latest_java)

    print(latest_java)

    java_dowload_link = latest_java[0]["binary"]["package"]["link"]
    java_checksum = latest_java[0]["binary"]["package"]["checksum"]
    java_release_name = f"{latest_java[0]["release_name"]}-jre"

    java_executable_path = f"{java_version_directory}/bin/java"
        
    if not os.path.exists(java_version_directory):
        Gio.File.new_for_uri(java_dowload_link).copy(Gio.File.new_for_path(java_zip_path), Gio.FileCopyFlags.OVERWRITE)
        with ZipFile(java_zip_path, "r") as java_zip:
            java_zip.extractall(java_directory)
            
        os.rename(f"{java_directory}/{java_release_name}", java_version_directory)

    #https://api.adoptium.net/v3/assets/latest/{java_version}/hotspot?architecture=x64&image_type=jre&os=windows&vendor=eclipse
    #https://api.adoptium.net/v3/binary/latest/21/ga/windows/x64/jre/hotspot/normal/eclipse

    progressbar.set_text(f"Récupération de la version {minecraft_version} du jeu")

    #minecraft_launcher_lib.fabric.install_fabric(minecraft_version, minecraft_directory)
    try:
        minecraft_launcher_lib.fabric.install_fabric(minecraft_version, minecraft_directory, loader_version, None, java_executable_path)
    except FileNotFoundError:
        progressbar.set_visible(False)
        play_button.set_visible(True)
        print("Erreur : Java n'est pas installé ou n'est pas accessible.")
        print("Veuillez installer Java (JDK 21+) et l'ajouter au PATH système.")
        return
    
    progressbar.set_text(f"Récupération de la version {modpack_version} du modpack")


    try:
        modpack_zip_path = f"{oracles_version_directory}/oracles-modpack-{modpack_version}.zip"

        remove_directory = ["mods", "config/fancymenu"]
        for directory in remove_directory:
            directory_path = f"{oracles_version_directory}/{directory}"
            if os.path.exists(directory_path):
                shutil.rmtree(directory_path)

        if not os.path.exists(modpack_zip_path):
            Gio.File.new_for_uri(modpack_download_link).copy(Gio.File.new_for_path(modpack_zip_path), Gio.FileCopyFlags.OVERWRITE)
        
        with ZipFile(modpack_zip_path, "r") as modpack_zip:
            modpack_zip.extractall(oracles_version_directory)
    except:
        print("Une erreur est survenu lors de l'installation du modpack")
        return
    
    progressbar.set_text("Récupération des données de lancement")

    try:
        start_minecraft_options = {
                "username": profile_data["name"],
                "uuid": profile_data["id"],
                "token": profile_data["access_token"],
                "executablePath": java_executable_path,
                "launcherName": "Oraclès Launcher",
                "launcherVersion": config["launcher"]["VERSION"],
                "gameDirectory": minecraft_directory
        }

        start_minecraft_command = minecraft_launcher_lib.command.get_minecraft_command(fabric_loader_version, minecraft_directory, start_minecraft_options)
    except:
        return
    
    progressbar.set_text("Lancement de minecraft")
    
    os.chdir(minecraft_directory)
    minecraft_proc = subprocess.Popen(start_minecraft_command, stdout=subprocess.PIPE, text=True)
    for line in minecraft_proc.stdout:
        update_vte()
    
    minecraft_proc.stdout.close()
    minecraft_proc.wait()

def update_vte():
    pass

def on_timeout(progressbar):
    progressbar.pulse()
    return True