from enum import Enum
from flask_login import UserMixin
from database import db


class Role(Enum):
    USER = 1
    CHAIRMAN = 2
    VICEDEAN = 3
    DEAN = 4
    ADMIN = 5


class User(db.Model, UserMixin):
    id = db.Column(db.Integer(), primary_key=True)
    university_id = db.Column(db.String(50), unique=True)
    fname = db.Column(db.String(50))
    lname = db.Column(db.String(50))
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    role = db.Column(db.Integer())
    code = db.Column(db.String(100))
    code_date = db.Column(db.DateTime)

    rank_id = db.Column(db.Integer(), db.ForeignKey('rank.id'))
    rank = db.relationship("Rank", foreign_keys=[rank_id])
    profile_id = db.Column(db.Integer(), db.ForeignKey('profile.id'))
    profile = db.relationship("Profile", foreign_keys=[profile_id])

    department_id = db.Column(db.Integer(), db.ForeignKey('department.id'))
    department = db.relationship("Department", foreign_keys=[department_id])
    department1_id = db.Column(
        db.Integer(), db.ForeignKey('department.id'), nullable=True)
    department1 = db.relationship("Department", foreign_keys=[department1_id])
    department2_id = db.Column(
        db.Integer(), db.ForeignKey('department.id'), nullable=True)
    department2 = db.relationship("Department", foreign_keys=[department2_id])

    course1_id = db.Column(
        db.Integer(), db.ForeignKey('course.id'), nullable=True)
    course1 = db.relationship("Course", foreign_keys=[course1_id])
    course2_id = db.Column(
        db.Integer(), db.ForeignKey('course.id'), nullable=True)
    course2 = db.relationship("Course", foreign_keys=[course2_id])
    course3_id = db.Column(
        db.Integer(), db.ForeignKey('course.id'), nullable=True)
    course3 = db.relationship("Course", foreign_keys=[course3_id])
    course4_id = db.Column(
        db.Integer(), db.ForeignKey('course.id'), nullable=True)
    course4 = db.relationship("Course", foreign_keys=[course4_id])
    course5_id = db.Column(
        db.Integer(), db.ForeignKey('course.id'), nullable=True)
    course5 = db.relationship("Course", foreign_keys=[course5_id])
    course6_id = db.Column(
        db.Integer(), db.ForeignKey('course.id'), nullable=True)
    course6 = db.relationship("Course", foreign_keys=[course6_id])
    course7_id = db.Column(
        db.Integer(), db.ForeignKey('course.id'), nullable=True)
    course7 = db.relationship("Course", foreign_keys=[course7_id])
    course8_id = db.Column(
        db.Integer(), db.ForeignKey('course.id'), nullable=True)
    course8 = db.relationship("Course", foreign_keys=[course8_id])

    journal_papers = db.Column(db.Integer)
    conf_papers = db.Column(db.Integer)
    supervision_activities = db.Column(db.Integer)

    # DirectTeaching
    dt111 = db.Column(db.Float)
    dt112 = db.Column(db.Float)
    dt113 = db.Column(db.Float)
    dt114 = db.Column(db.Float)
    dt121 = db.Column(db.Float)
    dt122 = db.Column(db.Float)
    dt123 = db.Column(db.Float)
    dt124 = db.Column(db.Float)
    dt13 = db.Column(db.Float)
    dt14 = db.Column(db.Float)
    dt15 = db.Column(db.Float)
    dt16 = db.Column(db.Float)
    dt17 = db.Column(db.Float)

    # GraduateStudies
    gs21 = db.Column(db.Float)
    gs22 = db.Column(db.Float)
    gs23 = db.Column(db.Float)
    gs24 = db.Column(db.Float)
    gs25 = db.Column(db.Float)

    # Research
    r31 = db.Column(db.Float)
    r321 = db.Column(db.Float)
    r322 = db.Column(db.Float)
    r33 = db.Column(db.Float)
    r34 = db.Column(db.Float)
    r35 = db.Column(db.Float)
    r36 = db.Column(db.Float)
    r37 = db.Column(db.Float)
    r38 = db.Column(db.Float)

    # University Communication
    uc41 = db.Column(db.Float)
    uc42 = db.Column(db.Float)
    uc43 = db.Column(db.Float)
    uc44 = db.Column(db.Float)
    uc45 = db.Column(db.Float)
    uc461 = db.Column(db.Float)
    uc462 = db.Column(db.Float)
    uc463 = db.Column(db.Float)
    uc47 = db.Column(db.Float)
    uc48 = db.Column(db.Float)
    uc49 = db.Column(db.Float)

    # Leadership
    l51 = db.Column(db.Float)
    l52 = db.Column(db.Float)
    l53 = db.Column(db.Float)
    l54 = db.Column(db.Float)
    l55 = db.Column(db.Float)
    l56 = db.Column(db.Float)
    l57 = db.Column(db.Float)
    l58 = db.Column(db.Float)

    def __init__(self, university_id, fname, lname, email, password, role, rank_id=1, profile_id=1, department_id=1, department1_id=1, department2_id=1, course1_id=None, course2_id=1, course3_id=1, course4_id=1, course5_id=1, course6_id=1, course7_id=1, course8_id=1, journal_papers=0, conf_papers=0, supervision_activities=0, dt111=0, dt112=0, dt113=0, dt114=0, dt121=0, dt122=0, dt123=0, dt124=0, dt13=0, dt14=0, dt15=0, dt16=0, dt17=0, gs21=0, gs22=0, gs23=0, gs24=0, gs25=0, r31=0, r321=0, r322=0, r33=0, r34=0, r35=0, r36=0, r37=0, r38=0, uc41=0, uc42=0, uc43=0, uc44=0, uc45=0, uc461=0, uc462=0, uc463=0, uc47=0, uc48=0, uc49=0, l51=0, l52=0, l53=0, l54=0, l55=0, l56=0, l57=0, l58=0):
        self.university_id = university_id
        self.fname = fname
        self.lname = lname
        self.email = email
        self.password = password
        self.role = role
        self.rank_id = rank_id
        self.profile_id = profile_id
        self.department_id = department_id
        self.department1_id = department1_id
        self.department2_id = department2_id

        self.course1_id = course1_id
        self.course2_id = course2_id
        self.course3_id = course3_id
        self.course4_id = course4_id
        self.course5_id = course5_id
        self.course6_id = course6_id
        self.course7_id = course7_id
        self.course8_id = course8_id

        self.journal_papers = journal_papers
        self.conf_papers = conf_papers
        self.supervision_activities = supervision_activities

        self.dt111 = dt111
        self.dt112 = dt112
        self.dt113 = dt113
        self.dt114 = dt114
        self.dt121 = dt121
        self.dt122 = dt122
        self.dt123 = dt123
        self.dt124 = dt124
        self.dt13 = dt13
        self.dt14 = dt14
        self.dt15 = dt15
        self.dt16 = dt16
        self.dt17 = dt17

        self.gs21 = gs21
        self.gs22 = gs22
        self.gs23 = gs23
        self.gs24 = gs24
        self.gs25 = gs25

        self.r31 = r31
        self.r321 = r321
        self.r322 = r322
        self.r33 = r33
        self.r34 = r34
        self.r35 = r35
        self.r36 = r36
        self.r37 = r37
        self.r38 = r38

        self.uc41 = uc41
        self.uc42 = uc42
        self.uc43 = uc43
        self.uc44 = uc44
        self.uc45 = uc45
        self.uc461 = uc461
        self.uc462 = uc462
        self.uc463 = uc463
        self.uc47 = uc47
        self.uc48 = uc48
        self.uc49 = uc49

        self.l51 = l51
        self.l52 = l52
        self.l53 = l53
        self.l54 = l54
        self.l55 = l55
        self.l56 = l56
        self.l57 = l57
        self.l58 = l58

    def __repr__(self) -> str:
        return f'<User {self.university_id}>'


class Rank(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(50))

    def __init__(self, name):
        self.name = name

    def __repr__(self) -> str:
        return id


class Profile(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(50), unique=True)
    direct_teaching = db.Column(db.Integer())
    direct_teaching_percent = db.Column(db.Integer())
    direct_teaching_minimum = db.Column(db.Integer())
    supervision = db.Column(db.Integer())
    supervision_percent = db.Column(db.Integer())
    research = db.Column(db.Integer())
    research_percent = db.Column(db.Integer())
    university_service = db.Column(db.Integer())
    university_service_percent = db.Column(db.Integer())
    lead_manage_admin = db.Column(db.Integer())
    lead_manage_admin_percent = db.Column(db.Integer())

    def __init__(self, name, direct_teaching, direct_teaching_percent, direct_teaching_minimum, supervision, supervision_percent, research, research_percent, university_service, university_service_percent, lead_manage_admin, lead_manage_admin_percent):
        self.name = name
        self.direct_teaching = direct_teaching
        self.direct_teaching_percent = direct_teaching_percent
        self.direct_teaching_minimum = direct_teaching_minimum
        self.supervision = supervision
        self.supervision_percent = supervision_percent
        self.research = research
        self.research_percent = research_percent
        self.university_service = university_service
        self.university_service_percent = university_service_percent
        self.lead_manage_admin = lead_manage_admin
        self.lead_manage_admin_percent = lead_manage_admin_percent

    def __repr__(self) -> str:
        return id


class Department(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    university_id = db.Column(db.String(50), unique=True)
    name = db.Column(db.String(50), unique=True)

    def __init__(self, university_id, name):
        self.university_id = university_id
        self.name = name

    def __repr__(self) -> str:
        return id


class CourseType(Enum):
    NORMAL = 1
    MASTER = 2
    PHD = 3
    LAB = 4
    EMBEDDED = 5


class Course(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    university_id = db.Column(db.String(50), unique=True)
    name = db.Column(db.String(50))
    credit = db.Column(db.Float())
    course_type = db.Column(db.Integer())

    department_id = db.Column(db.Integer(), db.ForeignKey('department.id'))
    department = db.relationship("Department", foreign_keys=[department_id])

    def __init__(self, university_id, name, credit, course_type, department_id):
        self.university_id = university_id
        self.name = name
        self.credit = credit
        self.course_type = course_type
        self.department_id = department_id

    def __repr__(self) -> str:
        return id
