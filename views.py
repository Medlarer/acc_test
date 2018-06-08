#!/usr/bin/env python


"""

"""

import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import json
import re
from flask import render_template
from flask import request
from flask import session
from flask import abort



RE_EMAIL = r"\w[-\w.+]*@([A-Za-z0-9][-A-Za-z0-9]+\.)+[A-Za-z]{2,14}"
RE_PHONE = r"(13|14|15|17|18|19)[0-9]{9}"


class Config:
    # celery config
    BROKER_URL = "amqp://127.0.0.1:5672"
    CELERY_RESULT_BACKEND = "amqp://127.0.0.1:5672"
    CELERY_TASK_SERIALIZER = "json"
    CELERY_RESULT_SERIALIZER = "json"
    CELERY_TASK_RESULT_EXPIRES = 24 * 60 * 60
    CELERY_ACCEPT_CONTENT = ["json"]

    # mysql config
    SQLALCHEMY_DATABASE_URI = "mysql://root:root123@127.0.0.1:3306/text"
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True

    # session config
    SECRET_KEY = "123456"


class DevelopConfig(Config):
    DEBUG = True


class ProductConfig(Config):
    pass


app = Flask(__name__)
app.config.from_object(DevelopConfig)
db = SQLAlchemy()
db.init_app(app)
app.config['SECRET_KEY'] = '123456'
BASE_DIR = os.path.dirname(os.path.abspath(__file__))


class User(db.Model):
    # table_name
    __tablename__ = "user_info"
    id = db.Column(db.Integer, primary_key=True)
    kkid = db.Column(db.String(80))
    company_name = db.Column(db.String(30))
    name = db.Column(db.String(20))
    position = db.Column(db.String(30))
    phone = db.Column(db.Integer, unique=True)
    email = db.Column(db.String(30))

    def __init__(self, kkid, name, company_name, position, phone, email):
        self.kkid = kkid
        self.name = name
        self.company_name = company_name
        self.position = position
        self.phone = phone
        self.email = email

    def __repr__(self):
        return "<Company:%s User:%s>" % (self.company_name, self.name)


@app.route("/index", methods=['GET'])
def index():
    # try:
    #     key_code = request.get_data()
    #     session["kkid"] = key_code
    #     if key_code:
    #         return render_template("index.html")
    # except Exception as e:
    #     return "Error: Need verification code, %s" % e.message
    print("sda1")
    return render_template("index.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    try:
        info = {"code": None, "message": None, "status": False}
        raw_data = request.get_data()
        loads_data = json.loads(raw_data)
        email = loads_data.get("email")
        real_email = re.match(RE_EMAIL, email)
        if not real_email:
            info["code"] = 401
            info["message"] = "Bad mailbox format"
            abort(401)
            return json.dumps(info)
        session["user_data"] = loads_data
        user_info = User(loads_data["kkty"], loads_data["company"],
                         loads_data["name"], loads_data["job"],
                         loads_data["phone"], loads_data["email"])
        db.session.add(user_info)
        db.session.commit()
        app.logger.info("Write to database successfully")
        info["code"] = 200
        info["status"] = True
        return json.dumps(info)
    except Exception as e:
        abort(e.message)


@app.route("/data", methods=["GET", ])
def data_input():
    pass


if __name__ == "__main__":
    app.run()