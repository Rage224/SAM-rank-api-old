from flask_restful import Resource
from common.psyonix_api import get_ranks_by_id
import common.globals as globals 

class PS4Player(Resource):
    def get(self, id):
        ranks = get_ranks_by_id(1, id, globals.session_id)
        if ranks == None:
            return {'error': 'error getting player'}, 500

        player = {
            'id': id,
            'platform': 0,
            'name': id,
        }
        player.update(ranks)
        globals.database.upsert_player(player)
        return player, 2000

    def post(self):
        pass