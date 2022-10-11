import csv
from models import User, Role, Rank, Profile, Department, Course
from database import db


def null_if(value):
    if value == 'NULL':
        return None
    else:
        return value


def format_errors(dictObj, indent=0):
    p = []
    p.append('<ul>\n')
    for k, v in dictObj.items():
        if isinstance(v, dict):
            p.append('<li>' + str(k) + ':')
            p.append(format_errors(v))
            p.append('</li>')
        else:
            p.append('<li>' + str(k) + ':' + str(v) + '</li>')
    p.append('</ul>\n')
    return '\n'.join(p)


def course_calc(course):
    if course.course_type == 1:
        effort = course.credit
    if course.course_type == 2:
        effort = course.credit*1.2
    if course.course_type == 3:
        effort = course.credit*1.5
    if course.course_type == 4:
        effort = course.credit*1.5
    if course.course_type == 5:
        effort = course.credit + 0.5

    return round(effort, 1)


def selection_calc(user):
    course1_credit = course_calc(
        user.course1) if user.course1 is not None else 0
    course2_credit = course_calc(
        user.course2) if user.course2 is not None else 0
    course3_credit = course_calc(
        user.course3) if user.course3 is not None else 0
    course4_credit = course_calc(
        user.course4) if user.course4 is not None else 0
    course5_credit = course_calc(
        user.course5) if user.course5 is not None else 0
    course6_credit = course_calc(
        user.course6) if user.course6 is not None else 0
    course7_credit = course_calc(
        user.course7) if user.course7 is not None else 0
    course8_credit = course_calc(
        user.course8) if user.course8 is not None else 0

    total = course1_credit + course2_credit + \
        course3_credit + course4_credit + course5_credit + \
        course6_credit + course7_credit + course8_credit

    return round(total, 1)


def load_users(path):
    with open(path + '/csv/user.csv') as cdv_file:
        csv_reader = csv.reader(cdv_file, delimiter=',')
        next(csv_reader, None)  # skip the headers
        for row in csv_reader:
            user = User(university_id=row[1], fname=row[2], lname=row[3],
                        email=row[4], password=row[5], role=row[6], rank_id=row[9], profile_id=row[10], department_id=row[11], department1_id=row[12], department2_id=row[13], course1_id=null_if(row[14]), course2_id=null_if(row[15]), course3_id=null_if(row[16]), course4_id=null_if(row[17]), course5_id=null_if(row[18]), course6_id=null_if(row[19]), course7_id=null_if(row[20]), course8_id=null_if(row[21]), journal_papers=row[22], conf_papers=row[23], supervision_activities=row[24], dt111=row[25], dt112=row[26], dt113=row[27], dt121=row[28], dt122=row[29], dt123=row[30], dt124=row[31], dt13=row[32], dt14=row[33], dt15=row[34], dt16=row[35], dt17=row[36], gs21=row[37], gs22=row[38], gs23=row[39], gs24=row[40], gs25=row[41], r31=row[42], r321=row[43], r322=row[44], r33=row[45], r34=row[46], r35=row[47], r36=row[48], r37=row[49], r38=row[50], uc41=row[51], uc42=row[52], uc43=row[53], uc44=row[54], uc45=row[55], uc461=row[56], uc462=row[57], uc463=row[58], uc47=row[59], uc48=row[60], uc49=row[61], l51=row[62], l52=row[63], l53=row[64], l54=row[65], l55=row[66], l56=row[67], l57=row[68], l58=row[69])
            db.session.add(user)
        db.session.commit()


def load_ranks(path):
    with open(path + '/csv/rank.csv') as cdv_file:
        csv_reader = csv.reader(cdv_file, delimiter=',')
        next(csv_reader, None)  # skip the headers
        for row in csv_reader:
            rank = Rank(name=row[1])
            db.session.add(rank)
        db.session.commit()


def load_profiles(path):
    with open(path + '/csv/profile.csv') as cdv_file:
        csv_reader = csv.reader(cdv_file, delimiter=',')
        next(csv_reader, None)  # skip the headers
        for row in csv_reader:
            profile = Profile(name=row[1], direct_teaching=row[2], direct_teaching_percent=row[3], direct_teaching_minimum=row[4], supervision=row[5], supervision_percent=row[6],
                              research=row[7], research_percent=row[8], university_service=row[9], university_service_percent=row[10], lead_manage_admin=row[11], lead_manage_admin_percent=row[12])
            db.session.add(profile)
        db.session.commit()


def load_departments(path):
    with open(path + '/csv/department.csv') as cdv_file:
        csv_reader = csv.reader(cdv_file, delimiter=',')
        next(csv_reader, None)  # skip the headers
        for row in csv_reader:
            department = Department(university_id=row[1], name=row[2])
            db.session.add(department)
        db.session.commit()


def load_courses(path):
    with open(path + '/csv/course.csv') as cdv_file:
        csv_reader = csv.reader(cdv_file, delimiter=',')
        next(csv_reader, None)  # skip the headers
        for row in csv_reader:
            course = Course(
                university_id=row[1], name=row[2], credit=row[3], course_type=row[4], department_id=row[5])
            db.session.add(course)
        db.session.commit()


def load_data(path):
    print("load_data is running!")
    load_ranks(path)
    load_profiles(path)
    load_departments(path)
    load_courses(path)
    load_users(path)
