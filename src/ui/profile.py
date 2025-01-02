import gi

gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")
gi.require_version("Gio", "2.0")

from gi.repository import Gtk, Adw, Gdk, Gio

class Profile():
    def __init__(self, window):
        self.profile_box = Gtk.Box(
            margin_top=50,
            orientation=Gtk.Orientation.VERTICAL,
            spacing=10
        )


        self.avatar_image = Gdk.Texture.new_from_file(Gio.File.new_for_path("data/default_profile_logo.png"))
        self.avatar = Adw.Avatar(
            size=100,
            custom_image=self.avatar_image,
            text="?",
            show_initials=True
        )
        self.profile_box.append(self.avatar)

        window.overlaysw.set_sidebar(self.profile_box)