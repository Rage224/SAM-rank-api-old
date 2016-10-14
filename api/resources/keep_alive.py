from flask_restful import Resource
import common.globals as globals
from common.psyonix_api import keep_alive 

class KeepAlive(Resource):
    def get(self):
        keep_alive(globals.session_id)
        return {"success": "sent keep alive request"}, 200

    def post(self):
        pass