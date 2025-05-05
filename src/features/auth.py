
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

import json
import os

from features.platform import Platform

platform = Platform()

def load_file():
    login_data = None

    if os.path.exists(platform.auth_file_path):
        # Importation des identifiants de connexion
        with open(platform.auth_file_path, 'r') as auth_file:
            profiles_data = json.load(auth_file)
        
        if len(profiles_data["profiles"]) != 0:
            for profile in profiles_data["profiles"]:
                if profile["profile"]["state"] == "ACTIVE":
                    login_data = profile
    
    print("Données utilisateur chargées !")
    return login_data

def add_profile(profiles_data):
    if os.path.exists(platform.auth_file_path):
        with open(platform.auth_file_path, 'w') as auth_file:
            json.dump(profiles_data, auth_file, indent=4)
            print("Les identifiants de connexion ont été enregistrés avec succès !")

def remove_profile(profile_id):
    if os.path.exists(platform.auth_file_path):
        # Importation des identifiants de connexion
        with open(platform.auth_file_path, 'r') as auth_file:
            profiles_data = json.load(auth_file)
        
        # Supprimer le profil correspondant
        new_profiles = []
        for profile in profiles_data["profiles"]:
            if profile.get("id") == profile_id:
                avatar_path = f"{platform.profiles_directory}/{profile["profile"]["avatar"]}.png"
                # Supprimer le fichier associé
                if os.path.exists(avatar_path):
                    os.remove(avatar_path)
                    print("Fichier supprimé")
                else:
                    print("Fichier non trouvé")
            else:
                new_profiles.append(profile)

        profiles_data["profiles"] = new_profiles
        
        with open(platform.auth_file_path, 'w') as auth_file:
            json.dump(profiles_data, auth_file, indent=4)
        
        #os.remove(f"{platform.profiles_directory}/{pro}")
        
def update_profile(profile_id, new_profile_data):
    if os.path.exists(platform.auth_file_path):
        # Importation des identifiants de connexion
        with open(platform.auth_file_path, 'r') as auth_file:
            profiles_data = json.load(auth_file)
        
        # Modifier le profil correspondant
        new_profiles = []
        for profile in profiles_data["profiles"]:
            if profile.get("id") == profile_id:
                new_profile_data["profile"] = profile["profile"]
                new_profiles.append(new_profile_data)
            else:
                new_profiles.append(profile)

        profiles_data["profiles"] = new_profiles
        
        with open(platform.auth_file_path, 'w') as auth_file:
            json.dump(profiles_data, auth_file, indent=4)