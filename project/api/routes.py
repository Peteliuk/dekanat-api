from flask import request

from flask_restful import Api
from flask_restful import Resource
from flask_restful import output_json

from project import app
from .handlers import Handler


class UnicodeApi(Api):
    """
    from here: https://github.com/flask-restful/flask-restful/issues/552
    """
    def __init__(self, *args, **kwargs):
        super(UnicodeApi, self).__init__(*args, **kwargs)
        self.app.config['RESTFUL_JSON'] = {
            'ensure_ascii': False
        }
        self.representations = {
            'application/json; charset=utf-8': output_json
        }


api = UnicodeApi(app)


class Index(Resource):
    @staticmethod
    def get():
        return {'OK': True}


class WhereSubject(Resource):
    @staticmethod
    def get(group_name, current_time):
        return {'answer': Handler().where_subject(group_name, current_time)}


class WhereFreeAuditorium(Resource):
    @staticmethod
    def get(current_time):
        return {'answer': Handler().where_free_auditorium(current_time)}


class WhatTeacher(Resource):
    @staticmethod
    def get(group_name, current_time):
        return {'answer': Handler().what_teacher(group_name, current_time)}


class WhatSubject(Resource):
    @staticmethod
    def get(group_name, current_time):
        return {'answer': Handler().what_subject(group_name, current_time)}


class IsTeacherHere(Resource):
    @staticmethod
    def get(teacher_name):
        return {'answer': Handler().is_teacher_here(teacher_name)}


api.add_resource(Index, '/')
api.add_resource(WhereSubject, '/api/where_subject/group=<string:group_name>&time=<string:current_time>')
api.add_resource(WhereFreeAuditorium, '/api/where_free_auditorium/time=<string:current_time>')
api.add_resource(WhatTeacher, '/api/what_teacher/group=<string:group_name>&time=<string:current_time>')
api.add_resource(WhatSubject, '/api/what_subject/group=<string:group_name>&time=<string:current_time>')
api.add_resource(IsTeacherHere, '/api/is_teacher_here/teacher=<string:teacher_name>')
