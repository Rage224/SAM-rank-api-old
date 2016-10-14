from flask_restful import Resource
import common.globals as globals
import keep_alive from common.psyonix_api

class KeepAlive(Resource):
    def get(self):
        keep_alive(globals.session_id)
        return {"success": "sent keep alive request"}, 200

    def post(self):
        pass