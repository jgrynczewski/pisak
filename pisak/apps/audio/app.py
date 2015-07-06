"""
Audio application main module
"""
from gi.repository import ClutterGst

import pisak
from pisak import app_manager
from pisak.libs import handlers
from pisak.libs.audio import data_loader

import pisak.libs.audio.handlers  # @UnusedImport
from pisak.libs.audio import widgets  # @UnusedImport


def prepare_folders_view(app, window, script, data):
    def _folder_tile_handler(tile, playlist_id):
        window.load_view("audio/playlist", {"playlist_id": playlist_id})

    data_source = script.get_object("data_source")
    data_source.item_handler = _folder_tile_handler
    handlers.button_to_view(window, script, "button_exit")


def prepare_playlist_view(app, window, script, data):
    script.get_object("data_source").data_set_id = data["playlist_id"]
    handlers.button_to_view(window, script, "button_exit")
    handlers.button_to_view(window, script, "button_return", "audio/main")


if __name__ == "__main__":
    pisak.init()
    ClutterGst.init()
    _audio_app = {
        "app": "audio",
        "type": "clutter",
        "views": [("playlist", prepare_playlist_view),
                  ("main", prepare_folders_view)]
    }
    data_loader.load_all()
    app_manager.run(_audio_app)
