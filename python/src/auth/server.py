import datetime
import jwt
from flask import Flask, request
from flask_mysqldb import MySQL

from config import settings

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


@server.route("/validate", methods=["POST"])
def validate():
    encoded_jwt = request.headers["Authorization"]
    if not encoded_jwt:
        return "missing credentials", 401

    encoded_jwt = encoded_jwt.split(" ")[1]

    try:
        decoded = jwt.decode(
            encoded_jwt, settings.secret_key, settings.algorithm
        )
    except:
        return "not authorized", 403

    return decoded, 200


def createJWT(username, secret, authz):
    return jwt.encode(
        {
            "username": username,
            "exp": datetime.datetime.now(tz=datetime.timezone.utc) +
                   datetime.timedelta(days=1),
            "iat": datetime.datetime.utcnow(),
            "admin": authz
        },
        secret,
        algorithm=settings.algorithm,
    )


if __name__ == "__main__":
    server.run(host="0.0.0.0", port=5000)
