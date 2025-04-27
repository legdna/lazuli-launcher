
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

import sys
import gi
import glob
import random

from features.platform import Platform
from features.play.terracles import Terracles

import pages.about as about

gi.require_version("Gtk", "4.0")
gi.require_version("Gdk", "4.0")
gi.require_version("Adw", "1")
gi.require_version("GLib", "2.0")
gi.require_version("Gio", "2.0")

from gi.repository import Gtk, GLib, Adw, Gio, Gdk # type: ignore

class Menu():
    def __init__(self, main_window):
        platform = Platform()

        self.notification_overlay = Adw.ToastOverlay()

        self.game_interface = Gtk.Box(
            orientation=Gtk.Orientation.VERTICAL
        )
        self.notification_overlay.set_child(self.game_interface)
        #main_window.select_game_interface.append(self.game_interface)

        self.game_page = Adw.NavigationPage.new_with_tag(
            tag="terracles",
            child=self.notification_overlay,
            title="Terraclès"
        )

        self.contentbox = Gtk.Overlay()
        self.game_interface.append(self.contentbox)

        self.about_button_icon = Gtk.Image.new_from_icon_name("help-about-symbolic")
        self.about_button_label = Gtk.Label.new("À propos")
        self.about_button_box = Gtk.Box(spacing=10)
        self.about_button_box.append(self.about_button_icon)
        self.about_button_box.append(self.about_button_label)


        self.about_button = Gtk.Button(
            child=self.about_button_box,
            halign=Gtk.Align.START,
            valign=Gtk.Align.END,
            margin_bottom=5,
            margin_start=5,
            css_classes=[
                "flat"
            ]
        )
        self.about_button.connect('clicked', lambda widget: platform.dialog(main_window, about.NativeAboutDialog, about.AdwAboutDialog, "show"))
        #self.contentbox.add_overlay(self.about_button)

        self.game_interface_box_menu = Gtk.Box(
            height_request=100,
            width_request=300,
            halign=Gtk.Align.CENTER,
            valign=Gtk.Align.CENTER,
            orientation=Gtk.Orientation.VERTICAL,
            hexpand=True,
            vexpand=True,
            spacing=10
        )
        self.contentbox.add_overlay(self.game_interface_box_menu)
        
        self.carousel = Adw.Carousel(
            interactive=False,
            css_classes=[
                "image-background"
            ]
        )

        # Ajoue des images d'arrière-plan
        backgrounds = glob.glob('data/background/terracles/*.bkg')
        random.shuffle(backgrounds)
        for background in backgrounds:
            print(background)
            image = Gtk.Picture(
                file=Gio.File.new_for_path(background),
                hexpand=True,
                vexpand=True,
                content_fit=Gtk.ContentFit.COVER
            )
            self.carousel.append(image)

        self.contentbox.set_child(self.carousel)

        self.previous_image_button = Gtk.Button(
            icon_name="go-previous-symbolic",
            halign=Gtk.Align.START,
            valign=Gtk.Align.CENTER,
            margin_start=20,
            css_classes=[
                "osd",
                "circular"
            ]
        )
        self.previous_image_button.connect("clicked", lambda widget: self.image_navigation_logic("previous"))
        self.contentbox.add_overlay(self.previous_image_button)

        self.next_image_button = Gtk.Button(
            icon_name="go-next-symbolic",
            halign=Gtk.Align.END,
            valign=Gtk.Align.CENTER,
            margin_end=20,
            css_classes=[
                "osd",
                "circular"
            ]
        )
        self.next_image_button.connect("clicked", lambda widget: self.image_navigation_logic("next"))
        self.contentbox.add_overlay(self.next_image_button)

        self.game_logo = Gtk.Picture.new_for_resource("/xyz/oraclesmc/OraclesLauncher/logos/terracles-logo.png")
        self.game_logo.set_size_request(50, 50)
        self.game_logo_max_size = Adw.Clamp(
            child=self.game_logo,
            maximum_size=400
        )
        self.game_interface_box_menu.append(self.game_logo_max_size)

        self.play_button_icon = Gtk.Image.new_from_icon_name("media-playback-start-symbolic")
        self.play_button_label = Gtk.Label.new("Jouer")
        self.play_button_box = Gtk.Box(spacing=10)
        self.play_button_box.append(self.play_button_icon)
        self.play_button_box.append(self.play_button_label)
        self.play_button = Gtk.Button(
            child=self.play_button_box,
            halign=Gtk.Align.CENTER,
            valign=Gtk.Align.CENTER,
            margin_top=20,
            css_classes=[
                "suggested-action",
                "pill",
                "title-3"
            ]
        )
        self.play_button.connect("clicked", lambda widget: Terracles().play(widget, self.notification_overlay))
        self.game_interface_box_menu.append(self.play_button)

        GLib.timeout_add(15000, self.image_auto_navigation)

    def show_home(self, main_window):
        main_window.select_game_interface.pop()
    
    def show_sidbar(self, button):
        if self.game_interface.get_show_sidebar() == False:
            self.game_interface.set_show_sidebar(True)
        else:
            self.game_interface.set_show_sidebar(False)
    def image_navigation_logic(self, action):
        # Obtient le nombre de page présent dans le carousel
        n_pages = self.carousel.get_n_pages()
        n_pages = n_pages - 1

        # Obtient la position de la page actuelle
        position = self.carousel.get_position()
        position = int(position)

        if action == "next":
            if position >= n_pages:
                n_page = 0
            else:
                n_page = position + 1
        elif action == "previous":
            if position <= 0:
                n_page = n_pages
            else:
                n_page = position - 1
        else:
            sys.exit("Error: action " + action + " does not exist")

        page = self.carousel.get_nth_page(n_page)
        self.carousel.scroll_to(page, True)

    def image_auto_navigation(self):
        self.image_navigation_logic("next")
        return GLib.SOURCE_CONTINUE