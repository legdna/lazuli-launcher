
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

import os
import signal

import features.utilities

import gi

gi.require_version("Adw", "1")

from gi.repository import Adw # type: ignore

def stop_oracles(stop_button, play_button, notification_overlay):
    if not features.utilities.is_process_running():
        return False

    oracles_pid = features.utilities.get_pid()
    os.kill(oracles_pid, signal.SIGTERM)

    stop_button.set_visible(False)
    play_button.set_visible(True)

    stop_process_notification = Adw.Toast(title="Oraclès a été arrêté avec succès !")
    notification_overlay.add_toast(stop_process_notification)
