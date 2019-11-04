#!/usr/bin/python3

from api.model import School

schools = [
    {
        'name': 'School of Agriculture & Agricultural Technology',
        'code': 'SAAT'
    },
    {
        'name': 'School of Basic Medical Sciences',
        'code': 'SBMS'
    },
    {
        'name': 'School of Computing & Information Technology',
        'code': 'SCIT'
    },
    {
        'name': 'School of Biological Sciences',
        'code': 'SOBS'
    },
    {
        'name': 'School of Engineering & Engineering Technology',
        'code': 'SEET'
    },
    {
        'name': 'School of Environmental Technology',
        'code': 'SOET'
    },
    {
        'name': 'School of Health Technology',
        'code': 'SOHT'
    },
    {
        'name': 'School of Management Technology',
        'code': 'SMAT'
    },
    {
        'name': 'School of Physical Sciences',
        'code': 'SOPS'
    },
    {
        'name': 'School of General Studies',
        'code': 'DGS'
    },
]


def populate_schools_table():
    try:
        for school in schools:
            if not School.exists(code=school['code']):
                School(name=school['name'], code=school['code']).save()
        print('schools table populated succefully')
    except Exception as e:
        print(f'Something failed {e}')


if __name__ == '__main__':
    populate_schools_table()
