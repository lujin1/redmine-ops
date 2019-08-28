from flask import Flask,request
from api.redmine import Reply_redmine
import logging
from api.job import *
from flasgger import Swagger
from flask_basicauth import BasicAuth

app = Flask(__name__)
app.register_blueprint(job_api)
app.register_blueprint(redmine_api)

Swagger(app)

app.config['BASIC_AUTH_USERNAME'] = 'admin'
app.config['BASIC_AUTH_PASSWORD'] = '123456'

app.config['BASIC_AUTH_FORCE'] = True  # 整个站点都验证

basic_auth = BasicAuth(app)

if __name__ == '__main__':
    scheduler.start()
    app.run(host='0.0.0.0')

