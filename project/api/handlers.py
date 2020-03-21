from project.models.functions import get_free_auds
from project.models.functions import get_subjects
from project.models.functions import get_teacher_name_by_id
from project.models.functions import create_db
from project.models.functions import update_db


class Handler:
    @staticmethod
    def where_subject(group_name, current_time):
        result = get_subjects(current_time, group_name).first()
        return result[1].aud if result else None

    @staticmethod
    def where_free_auditorium(current_time):
        result = get_free_auds(current_time)
        return [res.aud for res in result] if result else None

    @staticmethod
    def what_teacher(group_name, current_time):
        result = get_subjects(current_time, group_name).first()
        return get_teacher_name_by_id(result[0].teacher_id) if result else None

    @staticmethod
    def what_subject(group_name, current_time):
        result = get_subjects(current_time, group_name).first()
        return result[0].name if result else None

    @staticmethod
    def is_teacher_here(teacher_name):
        result = get_subjects(teacher_name=teacher_name).all()
        return [{'aud': res[1].aud, 'num': res[1].subject_num} for res in result] if result else None
