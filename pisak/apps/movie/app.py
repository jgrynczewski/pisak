'''
Module with app-specific code for movie player.
'''
from gi.repository import ClutterGst

import pisak
from pisak import app_manager
from pisak.libs import handlers
from pisak.libs.movie import widgets, model
import pisak.libs.movie.handlers  # @UnusedImport


def prepare_flat_view(app, window, script, data):
    def movie_tile_handler(tile, movie_id):
        window.load_view(
            "movie/player", {"movie_id": movie_id})

    data_source = script.get_object("library_data")
    data_source.item_handler = movie_tile_handler
    handlers.button_to_view(window, script, "button_start")


def prepare_player_view(app, window, script, data):
    movie_id = data.get("movie_id")
    library = model.get_library()
    movie = library.get_item_by_id(movie_id)
    movie_path = movie.path
    playback = script.get_object("playback")
    playback.filename = movie_path
    subs = model.find_subtitles(movie_path)
    if subs:
        playback.set_subtitle_from_file(subs)
    handlers.button_to_view(window, script, "button_exit")
    handlers.button_to_view(window, script, "button_library", "movie/main")


if __name__ == "__main__":
    pisak.init()
    ClutterGst.init()
    model.get_library()
    _movie_app = {
        "app": "movie",
        "type": "clutter",
        "views": [("player", prepare_player_view),
                  ("main", prepare_flat_view)]
    }
    app_manager.run(_movie_app)
