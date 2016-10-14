from flask import Flask, g
from flask_restful import Api
from resources.steam_player import SteamPlayer
from resources.ps4_player import PS4Player
from resources.player import Player
from common.database import Database
from db_url import db_url
import common.globals as globals

app = Flask(__name__)
api = Api(app)

globals.database = Database(db_url)
# set constants
globals.session_id, globals.steam_api_key = globals.database.get_constants()

api.add_resource(Player, '/player', '/player/')
api.add_resource(SteamPlayer, '/player/steam', '/player/steam/<string:id>')
api.add_resource(PS4Player, '/player/ps4', '/player/ps4/<string:id>')
app.run(host="0.0.0.0")

