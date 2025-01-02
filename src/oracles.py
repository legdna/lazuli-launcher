import sys
import gi
import minecraft_launcher_lib
import os
import glob
import random

from ui.platform import Platform
from ui.profile import Profile

gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")
gi.require_version("GLib", "2.0")
gi.require_version("Gio", "2.0")

from gi.repository import Gtk, GLib, Adw, Gio, Gdk

test_css = Gtk.CssProvider()
test_css.load_from_string(
    """
    .test-custom-1 {
        background: rgba(0,0,0,0.5);
        border-radius: 15px;
    }
    .image-background {
        opacity: 50%;
    }
    """
)

screen = Gdk.Display.get_default()
Gtk.StyleContext.add_provider_for_display(screen, test_css, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)

# instanciation de la classe Platform
platform = Platform()

# Initialisation des variriables de la méthode path
platform.path()

# Création du répertoire OraclesLauncher
os.makedirs(platform.appdata, exist_ok=True)

class MainWindow(platform.appwindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        app_name = "Oraclès Launcher"
        GLib.set_application_name(app_name)
        Adw.StyleManager.get_default().set_color_scheme(color_scheme=Adw.ColorScheme.FORCE_DARK)

        self.set_default_size(800, 450)
        self.set_size_request(800, 450)

        ##self.box1 = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        
        self.overlaysw = Adw.OverlaySplitView(
            collapsed=True,
            show_sidebar=False
        )

        profile = Profile(self)

        self.box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)

        platform.apparence(self)

        self.contentbox = Gtk.Overlay()
        self.box.append(self.contentbox)
        self.overlaysw.set_content(self.box)

        profile_button_logo = Gtk.Image(
            file="data/default_profile_logo.png",
            pixel_size=50,
            css_classes=[
                "lowres-icon"
            ]
        )
        self.profile_button = Gtk.Button(
            child=profile_button_logo,
            halign=Gtk.Align.START,
            valign=Gtk.Align.START,
            css_classes=[
                "flat"
            ]
        )
        #self.profile_button.set_icon_name("sidebar-show-symbolic")
        self.profile_button.connect('clicked', self.show_sidbar)
        self.contentbox.add_overlay(self.profile_button)

        self.about_button = Gtk.Button(
            label="Open",
            icon_name="help-about-symbolic",
            halign=Gtk.Align.END,
            valign=Gtk.Align.START,
            css_classes=[
                "flat"
            ]
        )
        self.about_button.connect('clicked', self.show_about)
        self.contentbox.add_overlay(self.about_button)

        self.clamp = Gtk.Box(
            height_request=100,
            width_request=300,
            halign=Gtk.Align.CENTER,
            valign=Gtk.Align.CENTER,
            orientation=Gtk.Orientation.VERTICAL,
            hexpand=True,
            vexpand=True,
            spacing=10,
            css_classes=[
                #"test-custom-1"
                #"osd",
                #"toolbar"
                #"round",
                #"background"
            ]
        )
        self.contentbox.add_overlay(self.clamp)
        
        self.carousel = Adw.Carousel(
            css_classes=[
                "image-background"
            ]
        )

        # Ajoue dee images d'arrière-plan
        backgrounds = glob.glob('data/background/*.bkg')
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

        #self.carousel.scroll_to(self.image2, True)

        self.contentbox.set_child(self.carousel)

        self.logo = Gtk.Picture.new_for_file(Gio.File.new_for_path("data/oracles-logo2.png"))
        self.logo.set_size_request(50, 50)
        self.logo.set_margin_bottom(30)
        self.clamp.append(self.logo)

        self.play_button_icon = Gtk.Image.new_from_icon_name("media-playback-start-symbolic")
        self.play_button_label = Gtk.Label.new("Jouer")
        self.play_button_box = Gtk.Box(spacing=10)
        self.play_button_box.append(self.play_button_icon)
        self.play_button_box.append(self.play_button_label)

        self.play_button = Gtk.Button(
            child=self.play_button_box,
            halign=Gtk.Align.CENTER,
            valign=Gtk.Align.CENTER,
            css_classes=[
                "suggested-action",
                "pill",
                "title-3"
            ]
        )
        self.clamp.append(self.play_button)

        self.connect("realize", lambda widget: platform.windows_theme(self, app_name))

    def show_sidbar(self, button):
        if self.overlaysw.get_show_sidebar() == False:
            self.overlaysw.set_show_sidebar(True)
        else:
            self.overlaysw.set_show_sidebar(False)
    
    def show_about(self, action):
        platform.about(self)

class OraclesLauncher(Adw.Application):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.connect('activate', self.on_activate)

    def on_activate(self, app):
        self.win = MainWindow(application=app)
        self.win.present()

app = OraclesLauncher(application_id="xyz.oraclesmc.OraclesLauncher")
exit_status = app.run(sys.argv)
sys.exit(exit_status)