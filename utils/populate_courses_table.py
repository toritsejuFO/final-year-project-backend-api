#!/usr/bin/python3

from api.model import Course

courses = [
    {
        'title': 'Computer Applications',
        'code': 'CSC201',
        'level': '200',
        'department_code': 'CSC',
        'semester': 'first',
        'units': '4'
    },
    {
        'title': 'Computer Applications 2',
        'code': 'CSC202',
        'level': '200',
        'department_code': 'CSC',
        'semester': 'second',
        'units': '3'
    },
    {
        'title': 'Computer Systems',
        'code': 'CSC301',
        'level': '300',
        'department_code': 'CSC',
        'semester': 'first',
        'units': '3'
    },
    {
        'title': 'Computer Organization',
        'code': 'CSC303',
        'level': '300',
        'department_code': 'CSC',
        'semester': 'first',
        'units': '3'
    },
    {
        'title': 'Data Structures and Algorithms',
        'code': 'CSC305',
        'level': '300',
        'department_code': 'CSC',
        'semester': 'first',
        'units': '3'
    },
    {
        'title': 'Operating Systems',
        'code': 'CSC307',
        'level': '300',
        'department_code': 'CSC',
        'semester': 'first',
        'units': '3'
    },
    {
        'title': 'Computer Architecture',
        'code': 'CSC302',
        'level': '300',
        'department_code': 'CSC',
        'semester': 'second',
        'units': '3'
    },
    {
        'title': 'File Systems',
        'code': 'CSC304',
        'level': '300',
        'department_code': 'CSC',
        'semester': 'second',
        'units': '3'
    },
    {
        'title': 'Survey of Programming Languages',
        'code': 'CSC306',
        'level': '300',
        'department_code': 'CSC',
        'semester': 'second',
        'units': '3'
    },
    {
        'title': 'System Design and Analysis',
        'code': 'CSC308',
        'level': '300',
        'department_code': 'CSC',
        'semester': 'second',
        'units': '3'
    },
    {
        'title': 'Compiler Construction',
        'code': 'CSC312',
        'level': '300',
        'department_code': 'CSC',
        'semester': 'second',
        'units': '3'
    },
    {
        'title': 'Computer Profession',
        'code': 'CSC401',
        'level': '400',
        'department_code': 'CSC',
        'semester': 'first',
        'units': '1'
    },
    {
        'title': 'Database Management Systems',
        'code': 'CSC403',
        'level': '400',
        'department_code': 'CSC',
        'semester': 'first',
        'units': '3'
    },
    {
        'title': 'Computer Hardware',
        'code': 'CSC405',
        'level': '400',
        'department_code': 'CSC',
        'semester': 'first',
        'units': '3'
    },
    {
        'title': 'Algorithms',
        'code': 'CSC407',
        'level': '400',
        'department_code': 'CSC',
        'semester': 'first',
        'units': '3'
    },
    {
        'title': 'Operating Systems 2',
        'code': 'CSC409',
        'level': '400',
        'department_code': 'CSC',
        'semester': 'first',
        'units': '3'
    },
    {
        'title': 'Software Engineering',
        'code': 'CSC501',
        'level': '500',
        'department_code': 'CSC',
        'semester': 'first',
        'units': '3'
    },
    {
        'title': 'Management Information System',
        'code': 'CSC503',
        'level': '500',
        'department_code': 'CSC',
        'semester': 'first',
        'units': '3'
    },
    {
        'title': 'Data Processing',
        'code': 'CSC505',
        'level': '500',
        'department_code': 'CSC',
        'semester': 'first',
        'units': '3'
    },
    {
        'title': 'Data Communication',
        'code': 'CSC507',
        'level': '500',
        'department_code': 'CSC',
        'semester': 'first',
        'units': '3'
    },
    {
        'title': 'Web Design',
        'code': 'CSC509',
        'level': '500',
        'department_code': 'CSC',
        'semester': 'first',
        'units': '3'
    },
    {
        'title': 'Artificial Intelligence',
        'code': 'CSC513',
        'level': '500',
        'department_code': 'CSC',
        'semester': 'first',
        'units': '3'
    },
    {
        'title': 'Automata Compatibility and Formal Languages',
        'code': 'CSC502',
        'level': '500',
        'department_code': 'CSC',
        'semester': 'second',
        'units': '3'
    },
    {
        'title': 'Interactive Computer Gaphics',
        'code': 'CSC504',
        'level': '500',
        'department_code': 'CSC',
        'semester': 'second',
        'units': '3'
    },
    {
        'title': 'Computer Networks',
        'code': 'CSC506',
        'level': '500',
        'department_code': 'CSC',
        'semester': 'second',
        'units': '3'
    },
    {
        'title': 'Systems Performance Evaluation',
        'code': 'CSC508',
        'level': '500',
        'department_code': 'CSC',
        'semester': 'second',
        'units': '3'
    },
    {
        'title': 'Modelling Simulation and Forcasting',
        'code': 'CSC510',
        'level': '500',
        'department_code': 'CSC',
        'semester': 'second',
        'units': '3'
    },

    # SCHOOL COURSES

    {
        'title': 'Entrepreneural Studies I',
        'code': 'ENS301',
        'level': '300',
        'department_code': 'DGS',
        'semester': 'first',
        'units': '2'
    },
    {
        'title': 'Entrepreneural Studies II',
        'code': 'ENS302',
        'level': '300',
        'department_code': 'DGS',
        'semester': 'second',
        'units': '2'
    },
    {
        'title': 'General Studies',
        'code': 'GST101',
        'level': '100',
        'department_code': 'DGS',
        'semester': 'first',
        'units': '2'
    },
    {
        'title': 'General Studies',
        'code': 'GST103',
        'level': '100',
        'department_code': 'DGS',
        'semester': 'first',
        'units': '1'
    },
    {
        'title': 'General Studies',
        'code': 'GST108',
        'level': '100',
        'department_code': 'DGS',
        'semester': 'second',
        'units': '1'
    },
    {
        'title': 'General Studies',
        'code': 'GST110',
        'level': '100',
        'department_code': 'DGS',
        'semester': 'second',
        'units': '1'
    },
    {
        'title': 'General Studies',
        'code': 'GST102',
        'level': '100',
        'department_code': 'DGS',
        'semester': 'second',
        'units': '1'
    },
    {
        'title': 'General Studies',
        'code': 'GST201',
        'level': '200',
        'department_code': 'DGS',
        'semester': 'second',
        'units': '2'
    },
]


def populate_courses_table():
    try:
        for course in courses:
            title = course['title']
            code = course['code']
            level = course['level']
            department_code = course['department_code']
            semester = course['semester']
            units = course['units']
            if not Course.exists(course_code=code):
                Course(title=title, code=code, level=level, units=units,
                    department_code=department_code, semester=semester).save()
        print('courses table populated successfully')
    except Exception as e:
        print(f'Something failed {e}')


if __name__ == '__main__':
    populate_courses_table()
