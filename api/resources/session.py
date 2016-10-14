from flask_restful import Resource, reqparse
import common.globals as globals 

parser = reqparse.RequestParser()
parser.add_argument('session_id')

class Session(Resource):
    def post(self):
        args = parser.parse_args()
        globals.database.update_session(args['session_id'])
        globals.session_id = args['session_id']
        return {"success": "updated session id"}, 200