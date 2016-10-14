from flask_restful import Resource
import common.globals as globals 

class Player(Resource):
    def get(self):
        return {"players": globals.database.get_players()}, 200

    def post(self):
        pass