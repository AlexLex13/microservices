import jwt, datetime, os
from flask import Flask, request
from flask_mysqldb import MySQL
from .config import settings

server = Flask(__name__)
mysql = MySQL(server)

server.config["MYSQL_HOST"] = settings.database_hostname
server.config["MYSQL_USER"] = settings.database_username
server.config["MYSQL_PASSWORD"] = settings.database_password
server.config["MYSQL_DB"] = settings.database_name
server.config["MYSQL_PORT"] = settings.database_port

@server.route("/login", methods=["POST"])
def login():
    auth = request.authorization
    if not auth:
        return "missing credentials", 401

    cur = mysql.connection.cursor()
    res = cur.execute(
        "SELECT email, password FROM user WHERE enmail=%s", (auth.username,)
    )

    if res:
        user_row = cur.fetchone()
        email = user_row[0]
        password = user_row[1]

        if auth.username != email or auth.password != password:
            return "invalid credentials", 401
        else:
            return createJWT(auth.username, settings.secret_key, True)
    else:
        return "invalid credentials", 401
