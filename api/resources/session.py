from flask_restful import Resource, reqparse
import common.globals as globals 

parser = reqparse.RequestParser()
parser.add_argument('session_id')

class Session(Resource):
    def post(self):
        args = parser.parse_args()
        update_session(args['task'])
        return {"success": "updated session id"}