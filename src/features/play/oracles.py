
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
import psutil
import requests

import features.auth
from features.platform import Platform
from features.utilities import Utilities
from features.status import PlayTime

import gi

gi.require_version("Adw", "1")
gi.require_version("Gio", "2.0")
gi.require_version("GLib", "2.0")
#gi.require_version("Soup", "3.0")

from gi.repository import GLib, Gio, Adw # type: ignore

platform = Platform()
utilities = Utilities()

LOCKFILE = f"{platform.oracles_directory}/oracles.lockfile"
LAUNCHER_CONFIG = None

profile_data = None
play_button = None
progressbar = None

def oracles(main_window, button, progress, profile_button, show_profile_menu, profile_page, notification_overlay):
    global profile_data, play_button, progressbar, LOCKFILE, LAUNCHER_CONFIG

    LAUNCHER_CONFIG = json.loads(Gio.resources_lookup_data("/xyz/oraclesmc/OraclesLauncher/config.json", Gio.ResourceLookupFlags.NONE).get_data().decode())

    if os.path.exists(LOCKFILE):
        with open(LOCKFILE) as f:
            oracles_pid = int(f.read())
        
        if psutil.pid_exists(oracles_pid):
            try:
                for arg in psutil.Process(oracles_pid).cmdline():
                    if arg == f'-Dminecraft.launcher.brand={LAUNCHER_CONFIG["launcher"]["NAME"]}':
                        is_running_notification = Adw.Toast(title="Oraclès est déjà en cours d'éxecution !")
                        notification_overlay.add_toast(is_running_notification)
                        return
            except:
                os.remove(LOCKFILE)

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


    progressbar_task_id = GLib.timeout_add(100, lambda widget: on_timeout(progressbar), GLib.PRIORITY_DEFAULT)
    main_window.navigation_menu_box.set_sensitive(False)
    profile_page.logout_button.set_sensitive(False)

    def after_launch_minecraft(_result, task):
        GLib.source_remove(progressbar_task_id)

        progressbar.set_visible(False)
        play_button.set_visible(True)

        profile_page.logout_button.set_sensitive(True)
        main_window.navigation_menu_box.set_sensitive(True)

        if not task.had_error():
            main_window.minimize()

    launch_minecraft_task = Gio.Task.new(callback=after_launch_minecraft)
    launch_minecraft_task.run_in_thread(launch_minecraft)

def launch_minecraft(task, object, any, cancellable):
    global profile_data, play_button, progressbar, LOCKFILE, LAUNCHER_CONFIG
    print(profile_data)

    CLIENT_ID = LAUNCHER_CONFIG["microsoft"]["CLIENT_ID"]
    REDIRECT_URL = LAUNCHER_CONFIG["microsoft"]["REDIRECT_URL"]

    #soup_session = Soup.Session()

    try:
        #refresh token
        profile_data = minecraft_launcher_lib.microsoft_account.complete_refresh(CLIENT_ID, None, REDIRECT_URL, profile_data["refresh_token"])
        features.auth.update_profile(profile_data["id"], profile_data)
        pass
    except:
        print("Erreur lors du renouvellement du profile utilisateur !")
        task.return_error(GLib.Error("Une erreur est survenu lors de l'installation du modpack"))
        return
        
    try:
        update_url = "https://oraclesmc.xyz/update.json"

        #get_latest_update_file = Soup.Message.new("GET", update_url)
        #latest_update_file = soup_session.send_and_read(get_latest_update_file).get_data().decode()
        #update_data = json.loads(latest_update_file)
        update_data = requests.get(update_url).json()
    except:
        task.return_error(GLib.Error("Une erreur est survenu lors de l'installation du modpack"))
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
    java_version_directory = f"{java_directory}/{java_version}"

    # Obtention de la dernière version de java
    latest_java_url = f"https://api.adoptium.net/v3/assets/latest/{java_version}/hotspot?architecture=x64&image_type=jre&os={platform.os_release}&vendor=eclipse"
    latest_java = requests.get(latest_java_url).json()

    #get_latest_java = Soup.Message.new("GET", latest_java_url)
    #latest_java = soup_session.send_and_read(get_latest_java).get_data().decode()
    #latest_java = json.loads(latest_java)

    print(latest_java)

    java_dowload_link = latest_java[0]["binary"]["package"]["link"]
    java_checksum = latest_java[0]["binary"]["package"]["checksum"]
    java_archive_path = f"{java_directory}/{latest_java[0]["binary"]["package"]["name"]}"
    java_release_name = f"{latest_java[0]["release_name"]}-jre"

    java_executable_path = f"{java_version_directory}/bin/java"
    
    if not os.path.exists(java_version_directory):
        Gio.File.new_for_uri(java_dowload_link).copy(Gio.File.new_for_path(java_archive_path), Gio.FileCopyFlags.OVERWRITE)
        match platform.os_release:
            case "windows":
                with ZipFile(java_archive_path, "r") as java_zip:
                    java_zip.extractall(java_directory)
            case "linux":
                import tarfile
                with tarfile.open(java_archive_path, "r:gz") as java_tar_gz:
                    java_tar_gz.extractall(java_directory)
        
        os.remove(java_archive_path)  
        os.rename(f"{java_directory}/{java_release_name}", java_version_directory)

    #https://api.adoptium.net/v3/assets/latest/{java_version}/hotspot?architecture=x64&image_type=jre&os=windows&vendor=eclipse
    #https://api.adoptium.net/v3/binary/latest/21/ga/windows/x64/jre/hotspot/normal/eclipse

    progressbar.set_text(f"Récupération de la version {minecraft_version} du jeu")

    #minecraft_launcher_lib.fabric.install_fabric(minecraft_version, minecraft_directory)
    try:
        minecraft_launcher_lib.fabric.install_fabric(minecraft_version, minecraft_directory, loader_version, None, java_executable_path)
    except FileNotFoundError:
        print("Erreur : Java n'est pas installé ou n'est pas accessible.")
        print("Veuillez installer Java (JDK 21+) et l'ajouter au PATH système.")

        task.return_error(GLib.Error("Une erreur est survenu lors de l'installation du modpack"))
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
        
        os.remove(modpack_zip_path)
    except:
        print("Une erreur est survenu lors de l'installation du modpack")
        task.return_error(GLib.Error("Une erreur est survenu lors de l'installation du modpack"))
        return
    
    progressbar.set_text("Récupération des données de lancement")

    try:
        start_minecraft_options = {
                "username": profile_data["name"],
                "uuid": profile_data["id"],
                "token": profile_data["access_token"],
                #"executablePath": java_executable_path,
                "launcherName": LAUNCHER_CONFIG["launcher"]["NAME"],
                "launcherVersion": LAUNCHER_CONFIG["launcher"]["VERSION"],
                "gameDirectory": minecraft_directory
        }

        start_minecraft_command = minecraft_launcher_lib.command.get_minecraft_command(fabric_loader_version, minecraft_directory, start_minecraft_options)
    except:
        task.return_error(GLib.Error("Une erreur est survenu lors de l'initialisation d'oraclès"))
        return
    
    progressbar.set_text("Lancement de minecraft")
    
    #os.chdir(minecraft_directory)

    # Crée le launcher avec les flags souhaités
    launcher = Gio.SubprocessLauncher.new(Gio.SubprocessFlags.STDOUT_PIPE | Gio.SubprocessFlags.STDERR_PIPE)

    # Définit le répertoire de travail du sous-processus
    launcher.set_cwd(minecraft_directory)

    # Lance le sous-processus
    minecraft_proc = launcher.spawnv(start_minecraft_command)
    minecraft_pid = minecraft_proc.get_identifier()

    with open(LOCKFILE, "w") as oracles_lockfile:
        oracles_lockfile.write(str(minecraft_pid))
    
    import time
    time.sleep(4.0)
    #minecraft_proc = subprocess.run(start_minecraft_command, stdout=subprocess.PIPE, text=True)
    #for line in minecraft_proc.stdout:
    #    update_vte()
    
    #minecraft_proc.stdout.close()
    #minecraft_proc.wait()

def on_timeout(progressbar):
    progressbar.pulse()
    return True