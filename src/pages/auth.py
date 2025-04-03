import gi
import minecraft_launcher_lib
import sys
from PIL import Image
import json

from features.platform import Platform
from features.utilities import Utilities

gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")
gi.require_version("GLib", "2.0")
gi.require_version("Gio", "2.0")

from gi.repository import Gtk, Adw, Gio, GLib # type: ignore

# instanciation des classes Platform et Utilities
platform = Platform()
utilities = Utilities()

class NativeAuthDialog(Gtk.Window):
    def __init__(self, parent, action, windows_theme, update_profile):
        super().__init__()

        # Configure le dialogue
        self.set_transient_for(parent)
        self.set_modal(True)
        self.set_default_size(300, 470)
        self.set_size_request(300, 470)
        self.set_resizable(False)

        if action == "login":
            title = "Se connecter"
            self.set_title(title)

            self.login
            self.login(title, windows_theme, update_profile)
        elif action == "logout":
            self.logout()
        else:
            sys.exit("Error: action " + action + " does not exist")
    
    def login(self, title, windows_theme, update_profile):
        def get_login_url():
            nonlocal login_url, state, code_verifier

            login_url, state, code_verifier = minecraft_launcher_lib.microsoft_account.get_secure_login_data(self.CLIENT_ID, self.REDIRECT_URL)

            get_login_url_task.return_boolean(True)

        def get_login_url_finish(task_object, async_result, any):
            nonlocal login_url

            # Ouvre l'url de connexion dans le navigateur
            login_url = Gtk.UriLauncher(uri=login_url+"&prompt=login")
            login_url.launch()

            self.login_service = Gio.SocketService()
            self.login_service.add_inet_port(8000, None)
            self.login_service.connect("incoming", get_login)

        def get_login(source_object, connection, random_args):
            def read_data(stream, result):
                try:
                    data = stream.read_bytes_finish(result)
                    if data.get_size() > 0:
                        lines = data.get_data().decode('utf-8').split('\r\n')
                        request_line = lines[0]
                        login_code = request_line.split(' ')[1].split(' HTTP')[0]
                        
                        print(f"Données reçues : {login_code}")
                        
                        output_stream = connection.get_output_stream()
                        redirect_url = "https://oraclesmc.xyz/auth"
                        response = f"HTTP/1.1 302 Found\r\nLocation: {redirect_url}\r\n\r\n".encode('utf-8')
                        output_stream.write_all(response)
                        output_stream.close_async(GLib.PRIORITY_DEFAULT, None, None)

                        # Fermer le serveur après avoir récupéré les données
                        self.login_service.stop()
                        self.login_service.close()
                        print("Serveur arrêté")

                        self.validate_login(state, code_verifier, update_profile, login_code)
                    else:
                        print("Connexion fermée")
                except GLib.Error as e:
                    print(f"Erreur lors de la lecture : {e.message}")
            
            print("Nouvelle connexion entrante")
    
            # Créer un flux d'entrée pour lire les données
            input_stream = connection.get_input_stream()
            input_stream.read_bytes_async(1024, GLib.PRIORITY_DEFAULT, None, read_data)

        gresource_data = Gio.resources_lookup_data("/xyz/oraclesmc/OraclesLauncher/config.json", Gio.ResourceLookupFlags.NONE)
        config = json.loads(gresource_data.get_data().decode())
        self.CLIENT_ID = config["microsoft"]["CLIENT_ID"]
        self.REDIRECT_URL = config["microsoft"]["REDIRECT_URL"]
        self.login_service = None

        login_url = None
        state = None
        code_verifier = None

        get_login_url_task = Gio.Task.new(None, None, get_login_url_finish, None)
        GLib.idle_add(get_login_url)

        login_box_margin = 20
        self.login_box = Gtk.Box(
            orientation=Gtk.Orientation.VERTICAL,
            valign=Gtk.Align.CENTER,
            margin_top=login_box_margin,
            margin_bottom=login_box_margin,
            margin_start=login_box_margin,
            margin_end=login_box_margin,
            spacing=20
        )

        self.login_avatar = Adw.Avatar(
            icon_name="avatar-default-symbolic",
            size=120
        )
        self.login_box.append(self.login_avatar)

        login_title_margin = 25
        self.login_title = Gtk.Label(
            label="Se connecter",
            margin_top=login_title_margin,
            margin_bottom=login_title_margin,
            css_classes=[
                "title-1"
            ]
        )
        self.login_box.append(self.login_title)

        self.login_spinner = Adw.Spinner(
            width_request=50,
            height_request=50
        )
        self.login_box.append(self.login_spinner)

        self.set_child(self.login_box)

        self.connect("realize", lambda widget: windows_theme(self, title))
        self.show()

    def validate_login(self, state, code_verifier, update_profile, login_entry_content=None):
        def get_login_data(get_login_data_task, object, any, cancellable):
            nonlocal auth_code, login_data

            try:
                auth_code = minecraft_launcher_lib.microsoft_account.parse_auth_code_url(login_entry_content, state)
            except AssertionError:
                print("Les states ne corresponde pas  !")

                # Annonce que la tache à échouer
                #get_login_data_task.return_boolean(False)
                return
            except KeyError:
                print("Url invalide !")

                # Annonce que la tache à échouer
                #get_login_data_task.return_boolean(False)
                return
            
            login_data = minecraft_launcher_lib.microsoft_account.complete_login(self.CLIENT_ID, None, self.REDIRECT_URL, auth_code, code_verifier)
            
            # Annonce que la tache est terminé
            get_login_data_task.return_boolean(True)

        def get_skin(result, task, any):
            nonlocal login_data


            print(login_data)
            print(result)
            print(any)

            def get_skin_finish(source_file, result):
                if source_file.copy_finish(result):
                    load_skin = Image.open(skin_dest_path)
                    profile_picture = load_skin.crop((8,8,16,16))
                    profile_picture = profile_picture.resize((64,64), Image.Resampling.NEAREST)
                    profile_picture.save(platform.launcher_directory+"/profile.png")

                    #login_avatar_image = Gdk.Texture.new_from_file(Gio.File.new_for_path(platform.oracles_directory+"/profile.png"))
                    #self.login_avatar.set_custom_image(login_avatar_image)
                    #self.login_title.set_label("Connecté")

                    with open(platform.auth_file_path, 'w') as auth_file:
                        json.dump(login_data, auth_file)
                        print("Les identifiants de connexion ont été enregistrés avec succès !")
                    
                    update_profile(login_data["name"])
                    self.close()

            if task.propagate_boolean():
                # Détermine le skin actif de l'utilisateur
                skin_src_uri = ""
                for skin in login_data["skins"]:
                    #print(skin)
                    if skin.get("state") == "ACTIVE":
                        skin_src_uri = skin.get("url")
                        break

                skin_dest_path = platform.oracles_directory+"/skin.png"

                # Télécharge le skin de l'utilisateur
                utilities.copy_file(skin_src_uri, skin_dest_path, "uri", get_skin_finish)

        auth_code = None
        login_data = None

        if login_entry_content == None:
            login_entry_content = self.login_entry.get_buffer().get_text()
        print(login_entry_content)

        get_login_data_task = Gio.Task.new(None, None, get_skin, None)
        get_login_data_task.run_in_thread(get_login_data)

    def logout(self):
        pass

class AdwAuthDialog():
    def __init__(self, parent):
        pass