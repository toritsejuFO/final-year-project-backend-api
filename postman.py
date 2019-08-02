from flask import json

from api import api
from run_api import app

app.config['SERVER_NAME'] = 'localhost:5000'
app.app_context().push()

urlvars = False
swagger = True

data = api.as_postman(urlvars=urlvars, swagger=swagger)
print(json.dumps(data))
