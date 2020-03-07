from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager

from .app_config import app

db = SQLAlchemy(app)
migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)


class Teachers(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(30), nullable=False, unique=True)


class Groups(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    group_name = db.Column(db.String(10), nullable=False, unique=True)


class Auditoriums(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    aud = db.Column(db.String(10), nullable=False)
    subject_num = db.Column(db.Integer, nullable=False)
    status = db.Column(db.Boolean, nullable=False, default=False)


class Subjects(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    teacher_id = db.Column(db.Integer, db.ForeignKey('teachers.id'), nullable=False)
    group_id = db.Column(db.Integer, db.ForeignKey('groups.id'), nullable=False)
    aud_id = db.Column(db.Integer, db.ForeignKey('auditoriums.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)


class Functions:
    @staticmethod
    def get_teacher_id(full_name):
        """
        :param full_name:           (string) teacher's full name
        :return:                    (int) teacher's id
        """
        return Teachers.query.get(full_name=full_name).id or None

    @staticmethod
    def get_group_id(group_name):
        """
        :param group_name:          (string) group's name
        :return:                    (int) group's id
        """
        return Groups.query.get(group_name=group_name).id or None

    @staticmethod
    def get_aud_id(aud, subject_num):
        return Auditoriums.query.get(aud=aud, subject_num=subject_num).id or None

    @staticmethod
    def insert_teachers(full_names):
        """
        Inserts full_name field in `teachers` table

        :param full_names:          (list<string>) list of teachers full names
        """
        for full_name in full_names:
            db.session.add(Teachers(full_name=full_name))
            db.session.commit()

    @staticmethod
    def insert_groups(group_names):
        """
        Inserts group_name field in `groups` table

        :param group_names:   (list<string>) list of groups names
        """
        for group_name in group_names:
            db.session.add(Groups(group_name=group_name))
            db.session.commit()

    @staticmethod
    def insert_auds(auds):
        """
        Inserts data into `auds` table

        :param auds:          (list<touple<string, int>>) list of auditoriums
        """
        for aud in auds:
            for data in aud:
                db.session.add(Auditoriums(aud=data[0], subject_num=data[1]))
                db.session.commit()

    @staticmethod
    def change_all_auds_status():
        auds = Auditoriums.query.filter_by(status=True).all()
        for aud in auds:
            aud.status = False
            db.session.commit()

    def insert_subjects(self, subjects):
        """
        Inserts data into `subjects` table and update auditorium status
        :param subjects:      (list<touple<(int) teacher_id, (int) group_id, (string) aud, (int) num, (string) name>>)
                              list of subjects
        """
        for subject in subjects:
            for data in subject:
                db.session.add(Subjects(teacher_id=self.get_teacher_id(data[0]), group_id=self.get_group_id(data[1]),
                                        aud_id=self.get_aud_id(data[2], data[3]), name=data[4]))
                aud = Auditoriums.query.get(aud=data[2], subject_num=data[3])
                aud.status = True
                db.session.commit()

    @staticmethod
    def delete_all():
        # db.session.query(Teachers).delete()
        # db.session.query(Groups).delete()
        # db.session.query(Auditoriums).delete()
        db.session.query(Subjects).delete()
        db.session.commit()


if __name__ == '__main__':
    manager.run()
