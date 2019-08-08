#!/usr/bin/python3

from api.model import Course

courses = [
    {
        'title': 'Computer Applications',
        'code': 'CSC201',
        'level': '200',
        'department_code': 'CSC',
        'semester': 'first'
    },
    {
        'title': 'Computer Applications 2',
        'code': 'CSC202',
        'level': '200',
        'department_code': 'CSC',
        'semester': 'second'
    },
    {
        'title': 'Computer Systems',
        'code': 'CSC301',
        'level': '300',
        'department_code': 'CSC',
        'semester': 'first'
    },
    {
        'title': 'Computer Organization',
        'code': 'CSC303',
        'level': '300',
        'department_code': 'CSC',
        'semester': 'first'
    },
    {
        'title': 'Data Structures and Algorithms',
        'code': 'CSC305',
        'level': '300',
        'department_code': 'CSC',
        'semester': 'first'
    },
    {
        'title': 'Operating Systems',
        'code': 'CSC307',
        'level': '300',
        'department_code': 'CSC',
        'semester': 'first'
    },
    {
        'title': 'Computer Architecture',
        'code': 'CSC302',
        'level': '300',
        'department_code': 'CSC',
        'semester': 'second'
    },
    {
        'title': 'File Systems',
        'code': 'CSC304',
        'level': '300',
        'department_code': 'CSC',
        'semester': 'second'
    },
    {
        'title': 'Survey of Programming Languages',
        'code': 'CSC306',
        'level': '300',
        'department_code': 'CSC',
        'semester': 'second'
    },
    {
        'title': 'System Design and Analysis',
        'code': 'CSC308',
        'level': '300',
        'department_code': 'CSC',
        'semester': 'second'
    },
    {
        'title': 'Compiler Construction',
        'code': 'CSC312',
        'level': '300',
        'department_code': 'CSC',
        'semester': 'second'
    },
    {
        'title': 'Computer Profession',
        'code': 'CSC401',
        'level': '400',
        'department_code': 'CSC',
        'semester': 'first'
    },
    {
        'title': 'Database Management Systems',
        'code': 'CSC403',
        'level': '400',
        'department_code': 'CSC',
        'semester': 'first'
    },
    {
        'title': 'Computer Hardware',
        'code': 'CSC405',
        'level': '400',
        'department_code': 'CSC',
        'semester': 'first'
    },
    {
        'title': 'Algorithms',
        'code': 'CSC407',
        'level': '400',
        'department_code': 'CSC',
        'semester': 'first'
    },
    {
        'title': 'Operating Systems 2',
        'code': 'CSC409',
        'level': '400',
        'department_code': 'CSC',
        'semester': 'first'
    },
    {
        'title': 'Software Engineering',
        'code': 'CSC501',
        'level': '500',
        'department_code': 'CSC',
        'semester': 'first'
    },
    {
        'title': 'Management Information System',
        'code': 'CSC503',
        'level': '500',
        'department_code': 'CSC',
        'semester': 'first'
    },
    {
        'title': 'Data Processing',
        'code': 'CSC505',
        'level': '500',
        'department_code': 'CSC',
        'semester': 'first'
    },
    {
        'title': 'Data Communication',
        'code': 'CSC507',
        'level': '500',
        'department_code': 'CSC',
        'semester': 'first'
    },
    {
        'title': 'Web Design',
        'code': 'CSC509',
        'level': '500',
        'department_code': 'CSC',
        'semester': 'first'
    },
    {
        'title': 'Artificial Intelligence',
        'code': 'CSC513',
        'level': '500',
        'department_code': 'CSC',
        'semester': 'first'
    },
    {
        'title': 'Automata Compatibility and Formal Languages',
        'code': 'CSC502',
        'level': '500',
        'department_code': 'CSC',
        'semester': 'second'
    },
    {
        'title': 'Interactive Computer Gaphics',
        'code': 'CSC504',
        'level': '500',
        'department_code': 'CSC',
        'semester': 'second'
    },
    {
        'title': 'Computer Networks',
        'code': 'CSC506',
        'level': '500',
        'department_code': 'CSC',
        'semester': 'second'
    },
    {
        'title': 'Systems Performance Evaluation',
        'code': 'CSC508',
        'level': '500',
        'department_code': 'CSC',
        'semester': 'second'
    },
    {
        'title': 'Modelling Simulation and Forcasting',
        'code': 'CSC510',
        'level': '500',
        'department_code': 'CSC',
        'semester': 'second'
    },
]


def populate_courses_table():
    for course in courses:
        title = course['title']
        code = course['code']
        level = course['level']
        department_code = course['department_code']
        semester = course['semester']
        Course(title=title, code=code, level=level, department_code=department_code, semester=semester).save()
    print('courses table populated successfully')


if __name__ == '__main__':
    populate_courses_table()
