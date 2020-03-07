from flask_restful import Api, Resource

from .app_config import app
from .tasks import update_database

api = Api(app)


class Index(Resource):
    def get(self):
        update_database()
        return {'OK': True}


api.add_resource(Index, '/')
