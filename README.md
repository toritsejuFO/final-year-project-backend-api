# Final Year Project Backend Api

## Required Software
* Python-3.x
* pip
* pipenv
* mysql (or any database software, DB connection URI must match though)

## How do I get set up
* `git clone https://github.com/toritsejuFO/final-year-project-backend-api.git`
* `cd final-year-project-backend-api`
* `git checkout dev` or `git checkout -b {new-branch}`
* `pipenv shell && pipenv install`
* `cp .env.sample .env` (edit appropriately)
* `flask run`

## Initial DB setup
Create a database that matches the one in your .env file.
Run the commands below that in order to populate DB

* `flask semester`
* `flask level`
* `flask schools`
* `flask departments`
* `flask courses`

## Running Unit Tests
* `flask test`

## Testing with postman
* `./utils/create_postman_collections.sh`

This will create a ***postman_collection*** file that you can now import to postman app to test the API