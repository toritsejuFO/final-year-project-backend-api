#!/usr/bin/python3

from api.model import Department

departments = [
    {
        'name': 'Agricultural Economics',
        'code': 'AEC',
        'school_code': 'SAAT'
    },
    {
        'name': 'Agricultural Extension',
        'code': 'AEX',
        'school_code': 'SAAT'
    },
    {
        'name': 'Anatomy',
        'code': 'ANA',
        'school_code': 'SBMS'
    },
    {
        'name': 'Physiology',
        'code': 'PSY',
        'school_code': 'SBMS'
    },
    {
        'name': 'Computer Science',
        'code': 'CSC',
        'school_code': 'SCIT'
    },
    {
        'name': 'Information Technology',
        'code': 'IFT',
        'school_code': 'SCIT'
    },
    {
        'name': 'Biology',
        'code': 'BIO',
        'school_code': 'SOBS'
    },
    {
        'name': 'Biochemistry',
        'code': 'BCH',
        'school_code': 'SOBS'
    },
    {
        'name': 'Petroleum Engineering',
        'code': 'PET',
        'school_code': 'SEET'
    },
    {
        'name': 'Chemical Engineering',
        'code': 'CHE',
        'school_code': 'SEET'
    },
    {
        'name': 'Architecture',
        'code': 'ARC',
        'school_code': 'SOET'
    },
    {
        'name': 'Surveying & Geoinformatics',
        'code': 'SVG',
        'school_code': 'SOET'
    },
    {
        'name': 'Optometry',
        'code': 'OPT',
        'school_code': 'SOHT'
    },
    {
        'name': 'Public Health',
        'code': 'PUH',
        'school_code': 'SOHT'
    },
    {
        'name': 'Maritime Management Technology',
        'code': 'MMT',
        'school_code': 'SMAT'
    },
    {
        'name': 'Project Management Technology',
        'code': 'PMT',
        'school_code': 'SMAT'
    },
    {
        'name': 'Mathematics',
        'code': 'MTH',
        'school_code': 'SOPS'
    },
    {
        'name': 'Physics',
        'code': 'PHY',
        'school_code': 'SOPS'
    },
    {
        'name': 'General Studies',
        'code': 'DGS',
        'school_code': 'DGS'
    },
]


def populate_departments_table():
    try:
        for department in departments:
            if Department.query.filter_by(code=school.code).count() > 0:
            continue
            name = department['name']
            code = department['code']
            school_code = department['school_code']
            if not Department.exists(department_code=code):
                Department(name=name, code=code, school_code=school_code).save()
        print('departments table populated successfully')
    except Exception as e:
        print(f'Something failed: {e}')


if __name__ == '__main__':
    populate_departments_table()
