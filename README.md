# Final Year Project Backend Api

## Required Software
* Python-3.x
* pip
* pipenv

## How do I get set up
* `git clone https://github.com/toritsejuFO/final-year-project-backend-api.git`
* `cd final-year-project-backend-api`
* `git checkout dev` or `git checkout -b {new-branch}`
* `pipenv shell && pipenv install`
* `cp .env.sample .env` (edit appropriately)
* `flask run`

## Testing with postman
* `./utils/create_postman_collections.sh`

This will create a ***postman_collection*** file that you can now import to postman app to test the API