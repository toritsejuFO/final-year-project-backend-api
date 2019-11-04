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
    try
        for level in levels:
            if not Level.exists(level=level)
                Level(level=level).save()
        print('levels table populated succefully')
    except Exception as e:
        print(f'Something failed {e}')


if __name__ == '__main__':
    populate_levels_table()
