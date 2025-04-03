import gi
import pages.auth as auth
from features.platform import Platform
from features.utilities import Utilities

gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")

from gi.repository import Gtk, Adw # type: ignore

platform = Platform()
utilities = Utilities()

class Profile():
    def __init__(self, ui, main_window, profile_button_image):
        self.main_window = main_window

        self.profile_button_image = profile_button_image

        self.profile_overlay = Gtk.Overlay()

        self.profile_title = Gtk.Label(
            label="Profile",
            margin_top=10,
            halign=Gtk.Align.CENTER,
            valign=Gtk.Align.START,
            css_classes=[
                "title-2"
            ]
        )
        self.profile_overlay.add_overlay(self.profile_title)

        self.close_profile_button = Gtk.Button(
            icon_name="go-previous-symbolic",
            halign=Gtk.Align.END,
            valign=Gtk.Align.START,
            margin_top=5,
            margin_end=5,
            css_classes=[
                "flat"
            ]
        )
        self.close_profile_button.connect('clicked', lambda widget: self.close_profile(self, ui))
        self.profile_overlay.add_overlay(self.close_profile_button)

        self.profile_box = Gtk.Box(
            orientation=Gtk.Orientation.VERTICAL,
            spacing=10,
            #halign=Gtk.Align.CENTER,
            valign=Gtk.Align.CENTER
        )
        self.profile_overlay.set_child(self.profile_box)

        #self.avatar_image = Gdk.Texture.new_from_file(Gio.File.new_for_path("data/default_profile_logo.png"))
        self.avatar = Gtk.Image(
            icon_name="default-minecraft-profile",
            pixel_size=90
        )
        self.profile_box.append(self.avatar)

        self.profile_name = Gtk.Label(
            label="Déconnecté",
            css_classes=[
                "title-1"
            ]
        )
        self.profile_box.append(self.profile_name)

        self.login_date = Gtk.Label(
            label="Temps de jeu : N/A",
            css_classes=[
                "title-4",
                "dimmed"
            ]
        )
        self.profile_box.append(self.login_date)

        self.login_button_icon = Gtk.Image.new_from_icon_name("login")
        self.login_button_label = Gtk.Label.new("Se connecter")
        self.login_button_box = Gtk.Box(spacing=10)
        self.login_button_box.append(self.login_button_icon)
        self.login_button_box.append(self.login_button_label)
        self.login_button = Gtk.Button(
            margin_top=40,
            halign=Gtk.Align.CENTER,
            valign=Gtk.Align.END,
            child=self.login_button_box,
            css_classes=[
                "suggested-action",
                #"circular",
                "pill",
                "title-2"
            ]
        )
        self.login_button.connect('clicked', lambda widget: platform.dialog(main_window, auth.NativeAuthDialog, auth.AdwAuthDialog, "login", self.update_profile))
        self.profile_box.append(self.login_button)

        ui.game_interface.set_sidebar(self.profile_overlay)

    def update_profile(self, profile_name):
        new_profile_image = platform.launcher_directory + "/profile.png"

        self.profile_button_image.set_from_file(new_profile_image)
        self.avatar.set_from_file(new_profile_image)

        self.profile_name.set_label(profile_name)

        # Supprime le bouton login
        self.login_button.hide()

        self.logout_button_icon = Gtk.Image.new_from_icon_name("logout")
        self.logout_button_label = Gtk.Label.new("Se déconnecter")
        self.logout_button_box = Gtk.Box(spacing=10)
        self.logout_button_box.append(self.logout_button_icon)
        self.logout_button_box.append(self.logout_button_label)
        self.logout_button = Gtk.Button(
            margin_top=40,
            halign=Gtk.Align.CENTER,
            valign=Gtk.Align.END,
            child=self.logout_button_box,
            css_classes=[
                "destructive-action",
                #"circular",
                "pill",
                "title-2"
            ]
        )
        self.logout_button.connect('clicked', lambda widget: platform.dialog(self.main_window, auth.NativeAuthDialog, auth.AdwAuthDialog, "login", self.update_profile))
        self.profile_box.append(self.logout_button)

    def close_profile(self, button, ui):
        ui.game_interface.set_show_sidebar(False)