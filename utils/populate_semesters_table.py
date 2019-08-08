#!/usr/bin/python3
from api.model import Semester

semesters = [
    'first',
    'second'
]

def populate_semesters_table():
    for semester in semesters:
        Semester(semester=semester).save()
    print('Semesters table populated successfully')

if __name__ == "__main__":
    populate_semesters_table()
