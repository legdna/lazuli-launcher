from discordrp import Presence
import time
import json
import gi

gi.require_version("Gio", "2.0")

from gi.repository import Gio # type: ignore

class DiscordRichPresence():
    def __init__(self):
        data = Gio.resources_lookup_data("/xyz/oraclesmc/OraclesLauncher/config.json", Gio.ResourceLookupFlags.NONE)
        self.config = json.loads(data.get_data().decode())
    
    def start(self, task, object, any, cancellable):
        client_id = self.config["discord"]["CLIENT_ID"]

        with Presence(client_id) as presence:
            print("Connected")
            presence.set(
                {
                    "timestamps": {"start": int(time.time())},
                }
            )
            print("Presence updated")

            while True:
                time.sleep(15)
            
            presence.clear()
            print("Discord presence cleared")

class PlayTime():
    def __init__(self):
        start_time = time.time()
        play_time = start_time - time.time()
        print(int(play_time))