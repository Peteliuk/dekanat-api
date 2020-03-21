from flask import session

from .models import db
from .models import Groups
from .models import Teachers
from .models import Auditoriums
from .models import Subjects
from .models import TimeBounds

from project.generators.subject_number_generator import get_generated_subject_num
from project.generators.lists_generator import get_generated_lists


def get_teacher_id(full_name):
    """
    :param full_name:           (string) teacher's full name
    :return:                    (int) teacher's id
    """
    teacher = Teachers.query.filter(Teachers.full_name.like(f'%{full_name}%')).first()
    return teacher.id if teacher else None


def get_group_id(group_name):
    """
    :param group_name:          (string) group's name
    :return:                    (int) group's id
    """
    group = Groups.query.filter_by(group_name=group_name).first()
    return group.id if group else None


def get_aud_id(aud, subject_num):
    """
    :param aud:                 (string) auditorium's identificator
    :param subject_num:         (int) subject's number
    :return:                    (int) auditorium's id
    """
    aud = Auditoriums.query.filter_by(aud=aud, subject_num=subject_num).first()
    return aud.id if aud else None


def get_time_bounds():
    return TimeBounds.query.all()


def get_teacher_name_by_id(teacher_id):
    """
    :return:                    (string) teacher's full name
    """
    teacher = Teachers.query.filter_by(id=teacher_id).first()
    return teacher.full_name if teacher else None


def insert_teachers(full_names):
    """
    Inserts full_name field in `teachers` table

    :param full_names:          (list<string>) list of teachers full names
    """
    db.session.add_all([Teachers(full_name=full_name) for full_name in full_names])
    db.session.commit()


def insert_groups(group_names):
    """
    Inserts group_name field in `groups` table

    :param group_names:   (list<string>) list of groups names
    """
    db.session.add_all([Groups(group_name=group_name) for group_name in group_names])
    db.session.commit()
    

def insert_auds(auds):
    """
    Inserts data into `auditoriums` table

    :param auds:          (list<touple<string, int>>) list of auditoriums
    """
    db.session.add_all([Auditoriums(aud=aud[0], subject_num=aud[1]) for aud in auds])
    db.session.commit()


def insert_subjects(subjects):
    """
    Inserts data into `subjects` table and update auditorium status
    :param subjects:      (list<touple<string, string, string, int, string>>)
                          list of subjects
    """
    for subject in subjects:
        db.session.add(Subjects(teacher_id=get_teacher_id(subject[0]),
                                group_id=get_group_id(subject[1]),
                                aud_id=get_aud_id(subject[2], subject[3]),
                                name=subject[4]))
        aud = Auditoriums.query.filter_by(aud=subject[2], subject_num=subject[3]).first()
        aud.status = True
    db.session.commit()


def insert_time_bounds(time_bounds):
    db.session.add_all([TimeBounds(start=tb[0], end=tb[1], num=tb[2]) for tb in time_bounds])
    db.session.commit()


def delete_all():
    db.session.query(Teachers).delete()
    db.session.query(Groups).delete()
    db.session.query(Auditoriums).delete()
    db.session.query(Subjects).delete()
    db.session.query(TimeBounds).delete()
    db.session.commit()


def get_subjects(current_time=None, group_name=None, teacher_name=None):
    """
    Generates `join` query of `subjects` and `auditoriums` tables

    :param current_time:        (string) string value of time in `%H:%M` format, like `20:20`
    :param group_name:          (string) group's name
    :param teacher_name:        (string) teacher's name
    :return:                    (list<Subjects, Auditoriums>) list of two filtered objects
    """
    query = db.session.query(Subjects, Auditoriums).join(Auditoriums, Subjects.aud_id == Auditoriums.id)    
    result = query.filter((Subjects.group_id == get_group_id(group_name)) |
                          (Subjects.teacher_id == get_teacher_id(teacher_name)))
    if not current_time:
        return result
    subject_num = get_generated_subject_num(current_time)
    return result.filter(Auditoriums.subject_num == subject_num)


def get_free_auds(current_time):
    subject_num = get_generated_subject_num(current_time)
    query = Auditoriums.query.filter_by(subject_num=subject_num, status=False).all()
    return query


def create_db():
    db.create_all()


def update_db():
    # Dictionary of generated lists
    lists = get_generated_lists()

    delete_all()
    insert_teachers(lists['teachers'])
    insert_groups(lists['groups'])
    insert_auds(lists['auds'])
    insert_subjects(lists['subjects'])
    insert_time_bounds(lists['time_bounds'])
