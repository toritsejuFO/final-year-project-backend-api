#!/usr/bin/python3

from api.model import Level

levels = [
    '100',
    '200',
    '300',
    '400',
    '500'
]


def populate_levels_table():
    for level in levels:
        Level(level=level).save()
    print('levels table populated succefully')


if __name__ == '__main__':
    populate_levels_table()
