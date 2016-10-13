from flask_restful import Resource
from common.steam_api import get_steam_name_by_id
from common.psyonix_api import get_ranks_by_id
import common.globals as globals 

class SteamPlayer(Resource):

    def get(self, id):
        ranks = get_ranks_by_id(0, id, globals.session_id)
        if ranks == None:
            return {'error': 'error getting player'}, 500

        name = get_steam_name_by_id(id, globals.steam_api_key)
        if name == None:
            return {'error': 'error getting steam name'}, 500
        
        player = {
            'id': id,
            'platform': 0,
            'name': name,
        }
        player.update(ranks)
        globals.database.upsert_player(player)
        return player, 2000

    def post(self):
        pass