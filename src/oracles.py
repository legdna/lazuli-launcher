import sys
import os
import darkdetect

from features.platform import Platform
from features.status import DiscordRichPresence

import pages.oracles.ui as oracles
import pages.terracles.ui as terracles
#import pages.about as about

def setup_icon_theme():
    if "__compiled__" in globals():
        base_path = os.path.dirname(sys.executable)
        datas_path = os.path.join(base_path, "share")
        
        print(base_path)
        print(datas_path)

        # Définir les variables d'environnement critiques
        os.environ["XDG_DATA_DIRS"] = datas_path + os.pathsep + os.environ.get("XDG_DATA_DIRS", "")
        #os.environ["GTK_THEME"] = "Adwaita:dark"
        
        print(os.getenv("XDG_DATA_DIRS"))

        # Configurer GSettings pour forcer le thème
        gsettings_schema_path = os.path.join(base_path, "share", "glib-2.0", "schemas")
        if os.path.exists(gsettings_schema_path):
            os.environ["GSETTINGS_SCHEMA_DIR"] = gsettings_schema_path
            #subprocess.run(["glib-compile-schemas", gsettings_schema_path])

# Appeler avant toute importation GTK !
setup_icon_theme()

import gi

gi.require_version("Gtk", "4.0")
gi.require_version("Gdk", "4.0")
gi.require_version("Adw", "1")
gi.require_version("GLib", "2.0")
gi.require_version("Gio", "2.0")

from gi.repository import Gtk, GLib, Adw, Gio, Gdk, GdkPixbuf # type: ignore

screen = Gdk.Display.get_default()

# Charger et enregistrer la ressource
resource = Gio.Resource.load("data/oracles.gresource")
resource._register()

# Ajouter le chemin de la ressource au thème d'icônes
theme = Gtk.IconTheme.get_for_display(screen)
theme.add_resource_path("/xyz/oraclesmc/OraclesLauncher/icons/hicolor")

#style_manager = Adw.StyleManager.get_default()
#style_manager.set_color_scheme(Adw.ColorScheme.FORCE_DARK)

css_provider = Gtk.CssProvider()
css_provider.load_from_resource("/xyz/oraclesmc/OraclesLauncher/oracles.css")

Gtk.StyleContext.add_provider_for_display(screen, css_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)

# instanciation de la classe Platform
platform = Platform()

# Création des répertoires OraclesLauncher
os.makedirs(platform.launcher_directory, exist_ok=True)
os.makedirs(platform.oracles_directory, exist_ok=True)
os.makedirs(platform.terracles_directory, exist_ok=True)


#GLib.setenv("GSK_RENDERER", "VULKAN", False)
GLib.setenv("GSK_DEBUG", "renderer", False)

class MainWindow(platform.appwindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        app_name = "Oraclès Launcher"
        GLib.set_application_name(app_name)

        #if darkdetect.isLight():
            #Adw.StyleManager.get_default().set_color_scheme(color_scheme=Adw.ColorScheme.FORCE_LIGHT)
        #else:
            #Adw.StyleManager.get_default().set_color_scheme(color_scheme=Adw.ColorScheme.FORCE_DARK)

        self.set_default_size(1000, 550)
        self.set_size_request(1000, 550)

        self.main_window_box = Gtk.Box(
            orientation=Gtk.Orientation.VERTICAL
        )

        self.main_window_view = Adw.OverlaySplitView(
            collapsed=False,
            show_sidebar=True,
            hexpand=True,
            vexpand=True
        )
        self.main_window_box.append(self.main_window_view)

        self.main_menu_box = Gtk.Box(
            orientation=Gtk.Orientation.VERTICAL,
            halign=Gtk.Align.CENTER,
            valign=Gtk.Align.CENTER
        )

        self.launcher_logo = Gtk.Image(
            icon_name="oracles",
            #file="data/oracles.png",
            pixel_size=130,
            css_classes=[
                "lowres-icon"
            ]
        )
        self.main_menu_box.append(self.launcher_logo)

        self.launcher_title = Gtk.Label(
            label="Oraclès Launcher",
            margin_top=20,
            css_classes=[
                "title-1"
            ]
        )
        self.main_menu_box.append(self.launcher_title)

        self.select_game_interface = Adw.NavigationView()
        #self.select_game_interface.add(self.main_menu_box)
        self.main_window_view.set_content(self.select_game_interface)

        self.main_menu = Adw.NavigationPage.new_with_tag(
            tag="home",
            child=self.main_menu_box,
            title="Main Menu"
        )
        self.select_game_interface.add(self.main_menu)

        # ------------------------------------------------------------------------------------
        # > -- SIDEBAR -- <
        # ------------------------------------------------------------------------------------

        sidebar_bouton_image_size = 40
        sidebar_button_title_box_width = 40
        sidebar_button_title_box_height = 50

        self.main_window_view.set_min_sidebar_width(40)
        self.main_window_view.set_max_sidebar_width(240)

        self.navigation_menu_box = Gtk.CenterBox(
            orientation=Gtk.Orientation.VERTICAL,
            vexpand=True,
            margin_top=10,
            margin_bottom=10,
            margin_start=10,
            margin_end=10
        )
        self.main_window_view.set_sidebar(self.navigation_menu_box)

        self.home_box = Gtk.Box(
            orientation=Gtk.Orientation.VERTICAL,
            spacing=10
        )
        self.navigation_menu_box.set_start_widget(self.home_box)

        self.sidebar_box = Gtk.Box(
            orientation=Gtk.Orientation.VERTICAL,
            spacing=10
        )
        self.navigation_menu_box.set_center_widget(self.sidebar_box)

        self.settings_box = Gtk.Box(
            orientation=Gtk.Orientation.VERTICAL,
            spacing=10
        )
        self.navigation_menu_box.set_end_widget(self.settings_box)

        # Tableau contenant les boutons de la sidebar
        self.sidebar_buttons = []

        # BOUTON HOME

        self.home_button_icon = Gtk.Image(
            icon_name="home-button-symbolic",
            pixel_size=sidebar_bouton_image_size
        )
        self.home_button_label = Gtk.Label(
            label="Accueil",
            halign=Gtk.Align.START,
            css_classes=["title-4"]
        )
        self.home_button_description = Gtk.Label(
            label="Retourner à l'écran d'accueil",
            css_classes=["dimmed"]
        )
        self.home_button_title_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, valign=Gtk.Align.CENTER)
        self.home_button_title_box.append(self.home_button_label)
        self.home_button_title_box.append(self.home_button_description)
        self.home_button_box = Gtk.Box(
            spacing=15
        )
        self.home_button_box.set_size_request(sidebar_button_title_box_width, sidebar_button_title_box_height)
        self.home_button_box.append(self.home_button_icon)
        self.home_button_box.append(self.home_button_title_box)
        self.home_button = Gtk.Button(
            valign=Gtk.Align.END,
            hexpand=True,
            child=self.home_button_box
        )
        self.home_button.connect('clicked', lambda widget: self.navigation_menu_logics("go-to-home", None, widget))
        self.home_box.append(self.home_button)
        self.sidebar_buttons.append(self.home_button)

        # Séparateur

        self.home_box_separator = Gtk.Separator.new(Gtk.Orientation.HORIZONTAL)
        self.home_box.append(self.home_box_separator)

        # Bouton Oraclès

        self.oracles_button_icon = Gtk.Image(
            icon_name="oracles",
            #file="data/oracles.png",
            pixel_size=sidebar_bouton_image_size
        )
        self.oracles_button_label = Gtk.Label(
            label="Oraclès",
            halign=Gtk.Align.START,
            css_classes=["title-4"]
        )
        self.oracles_button_description = Gtk.Label(
            label="Un serveur minecraft moddé",
            css_classes=["dimmed"]
        )
        self.oracles_button_title_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, valign=Gtk.Align.CENTER)
        self.oracles_button_title_box.append(self.oracles_button_label)
        self.oracles_button_title_box.append(self.oracles_button_description)
        self.oracles_button_box = Gtk.Box(
            spacing=15
        )
        self.oracles_button_box.set_size_request(sidebar_button_title_box_width, sidebar_button_title_box_height)
        self.oracles_button_box.append(self.oracles_button_icon)
        self.oracles_button_box.append(self.oracles_button_title_box)
        self.oracles_button = Gtk.Button(
            valign=Gtk.Align.END,
            hexpand=True,
            child=self.oracles_button_box,
            css_classes=["flat"]
        )
        self.oracles_button.connect('clicked', lambda widget: self.navigation_menu_logics("go-to-page", oracles.Menu(self).game_page, widget))
        self.home_box.append(self.oracles_button)
        self.sidebar_buttons.append(self.oracles_button)

        # Bouton Terraclès

        self.terracles_button_icon = Gtk.Image(
            icon_name="terracles",
            pixel_size=sidebar_bouton_image_size
        )
        self.terracles_button_label = Gtk.Label(
            label="Terraclès",
            halign=Gtk.Align.START,
            css_classes=["title-4"]
        )
        self.terracles_button_description = Gtk.Label(
            label="Un serveur survie terraria",
            css_classes=["dimmed"]
        )
        self.terracles_button_title_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, valign=Gtk.Align.CENTER)
        self.terracles_button_title_box.append(self.terracles_button_label)
        self.terracles_button_title_box.append(self.terracles_button_description)
        self.terracles_button_box = Gtk.Box(spacing=15)
        self.terracles_button_box.set_size_request(sidebar_button_title_box_width, sidebar_button_title_box_height)
        self.terracles_button_box.append(self.terracles_button_icon)
        self.terracles_button_box.append(self.terracles_button_title_box)
        self.terracles_button = Gtk.Button(
            valign=Gtk.Align.END,
            hexpand=True,
            child=self.terracles_button_box,
            css_classes=["flat"]
        )
        self.terracles_button.connect('clicked', lambda widget: self.navigation_menu_logics("go-to-page", terracles.Menu(self).game_page, widget))
        self.home_box.append(self.terracles_button)
        self.sidebar_buttons.append(self.terracles_button)

        # Séparateur

        self.settings_box_separator = Gtk.Separator.new(Gtk.Orientation.HORIZONTAL)
        self.settings_box.append(self.settings_box_separator)

        self.unfold_button_icon = Gtk.Image(
            #resource="/xyz/oraclesmc/OraclesLauncher/icons/application-exit-rtl-symbolic.symbolic.png",
            icon_name="close-menu",
            pixel_size=sidebar_bouton_image_size
        )
        self.unfold_button_label = Gtk.Label(
            label="Replier",
            halign=Gtk.Align.START,
            css_classes=["title-4"]
        )
        self.unfold_button_description = Gtk.Label(
            label="Replier le menu",
            css_classes=["dimmed"]
        )
        self.unfold_button_title_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, valign=Gtk.Align.CENTER)
        self.unfold_button_title_box.append(self.unfold_button_label)
        self.unfold_button_title_box.append(self.unfold_button_description)
        self.unfold_button_box = Gtk.Box(spacing=15)
        self.unfold_button_box.set_size_request(sidebar_button_title_box_width, sidebar_button_title_box_height)
        self.unfold_button_box.append(self.unfold_button_icon)
        self.unfold_button_box.append(self.unfold_button_title_box)
        self.unfold_button = Gtk.Button(
            valign=Gtk.Align.END,
            hexpand=True,
            child=self.unfold_button_box,
            css_classes=["flat"]
        )
        self.unfold_button.connect('clicked', lambda widget: self.navigation_menu_logics("show-side-menu", None, None))
        self.settings_box.append(self.unfold_button)
        self.sidebar_buttons.append(self.unfold_button)

        # Apparence de la fenêtre
        platform.apparence(self)

        drp_task = Gio.Task.new()
        drp_task.run_in_thread(DiscordRichPresence().start)
        # Utilities().thread_manager(DiscordRichPresence, self.get_application().threads, self.get_application().stop_event)

        self.connect("realize", lambda widget: platform.windows_theme(self, app_name))
    
    def navigation_menu_logics(self, action:str, new_page=None, clicked_button=None):
        def button_title_box(action):
            if action == "hide":
                self.main_window_view.set_max_sidebar_width(40)
                self.home_button_title_box.set_visible(False)
                self.oracles_button_title_box.set_visible(False)
                self.terracles_button_title_box.set_visible(False)
                self.unfold_button_title_box.set_visible(False)
                self.unfold_button_icon.set_from_icon_name("show-menu")
            elif action == "show":
                self.main_window_view.set_max_sidebar_width(240)
                self.home_button_title_box.set_visible(True)
                self.oracles_button_title_box.set_visible(True)
                self.terracles_button_title_box.set_visible(True)
                self.unfold_button_title_box.set_visible(True)
                self.unfold_button_icon.set_from_icon_name("close-menu")

        page_tag = self.select_game_interface.get_visible_page().get_tag()

        if action == "show-side-menu":
            if self.home_button_title_box.get_visible():
                button_title_box("hide")
            else:
                button_title_box("show")
            return

        if new_page != None and new_page.get_tag() == page_tag:
            return

        print(page_tag)
        print(clicked_button)

        if clicked_button != None:
            clicked_button.remove_css_class("flat")
            for button in self.sidebar_buttons:
                if clicked_button != button:
                    button.add_css_class("flat")

        if page_tag != "home":
            if action == "go-to-home":
                self.select_game_interface.pop()
                button_title_box("show")
            elif action == "go-to-page" and new_page != None:
                self.select_game_interface.pop()
                self.select_game_interface.push(new_page)
        else:
            if action == "go-to-page" and new_page != None:
                #self.main_window_view.set_show_sidebar(False)
                button_title_box("hide")
                self.select_game_interface.push(new_page)

    def show_about(self, action):
        platform.about(self)

class OraclesLauncher(Adw.Application):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.connect('activate', self.on_activate)

    def on_activate(self, app):
        self.win = MainWindow(application=app)
        #self.win.connect("close-request", self.on_window_close)
        self.win.present()

app = OraclesLauncher(application_id="xyz.oraclesmc.OraclesLauncher")
exit_status = app.run(sys.argv)
sys.exit(exit_status)