#!/usr/bin/python3
from api.model import Semester

semesters = [
    'first',
    'second'
]

def populate_semesters_table():
    try:
        for semester in semesters:
            if not Semester.exists(semester=semester):
                Semester(semester=semester).save()
        print('Semesters table populated successfully')
    except Exception as e:
        print(f'Something failed {e}')

if __name__ == "__main__":
    populate_semesters_table()
