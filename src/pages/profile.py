
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
import pages.auth as auth
from features.platform import Platform

gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")

from gi.repository import Gtk, Adw # type: ignore

platform = Platform()

class Profile():
    def __init__(self, ui, main_window, profile_button_image, login_data):
        self.profile_button_image = profile_button_image

        self.profile_overlay = Gtk.Overlay(
            
        )

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
            width_request=270,
            spacing=10,
            #halign=Gtk.Align.CENTER,
            valign=Gtk.Align.CENTER
        )
        self.profile_overlay.set_child(self.profile_box)

        #self.avatar_image = Gdk.Texture.new_from_file(Gio.File.new_for_path("data/default_profile_logo.png"))
        self.avatar = Gtk.Image(

            pixel_size=90
        )
        self.profile_box.append(self.avatar)

        self.profile_name = Gtk.Label(
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
                "pill",
                "title-2"
            ]
        )
        self.login_button.connect('clicked', lambda widget: auth.NativeAuthDialog(main_window, "login", self.update_profile))
        self.profile_box.append(self.login_button)

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
                "pill",
                "title-2"
            ]
        )
        self.logout_button.connect('clicked', lambda widget: auth.NativeAuthDialog(main_window, "logout", self.update_profile))
        self.profile_box.append(self.logout_button)

        self.update_profile(login_data)
        
        ui.game_interface.set_sidebar(self.profile_overlay)

    def update_profile(self, login_data):
        avatar_image = "default-minecraft-profile"

        if login_data != None:
            avatar_image = f"{platform.profiles_directory}/{login_data["profile"]["avatar"]}.png"

            self.avatar.set_from_file(avatar_image)
            self.profile_button_image.set_from_file(avatar_image)
            self.profile_name.set_label(login_data["name"])
            
            self.login_button.set_visible(False)
            self.logout_button.set_visible(True)
        else: 
            self.avatar.set_from_icon_name(avatar_image)
            self.profile_button_image.set_from_icon_name(avatar_image)
            self.profile_name.set_label("Déconnecté")

            self.logout_button.set_visible(False)
            self.login_button.set_visible(True)

    def close_profile(self, button, ui):
        ui.game_interface.set_show_sidebar(False)