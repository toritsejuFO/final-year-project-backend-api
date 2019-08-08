from run_api import app
from utils.populate_departments_table import populate_departments_table
from utils.populate_levels_table import populate_levels_table
from utils.populate_schools_table import populate_schools_table
from utils.populate_semesters_table import populate_semesters_table
from utils.populate_courses_table import populate_courses_table


@app.cli.command()
def levels():
    populate_levels_table()

@app.cli.command()
def departments():
    populate_departments_table()

@app.cli.command()
def schools():
    populate_schools_table()

@app.cli.command()
def semesters():
    populate_semesters_table()

@app.cli.command()
def courses():
    populate_courses_table()
