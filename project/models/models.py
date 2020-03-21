from project import app
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager


db = SQLAlchemy(app)
migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)


class Teachers(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(40), nullable=False, unique=True)


class Groups(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    group_name = db.Column(db.String(20), nullable=False, unique=True)


class Auditoriums(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    aud = db.Column(db.String(30), nullable=False)
    subject_num = db.Column(db.Integer, nullable=False)
    status = db.Column(db.Boolean, nullable=False, default=False)


class Subjects(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    teacher_id = db.Column(db.Integer, db.ForeignKey('teachers.id'), nullable=False)
    group_id = db.Column(db.Integer, db.ForeignKey('groups.id'), nullable=False)
    aud_id = db.Column(db.Integer, db.ForeignKey('auditoriums.id'), nullable=False)
    name = db.Column(db.String(150), nullable=False)


class TimeBounds(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    start = db.Column(db.String(5), nullable=False)
    end = db.Column(db.String(5), nullable=False)
    num = db.Column(db.Integer, nullable=False)
