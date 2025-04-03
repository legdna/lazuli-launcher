class Oracles():
    def __init__(self):
        pass
    def play(self, play_button):
        pass

import gi
gi.require_version('Gtk', '4.0')
from gi.repository import Gtk, GLib # type: ignore
from urllib.parse import urlparse, parse_qs