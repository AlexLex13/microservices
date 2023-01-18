import datetime
import os
import jwt
from flask import Flask, request
from flask_mysqldb import MySQL

server = Flask(__name__)
mysql = MySQL(server)

server.config["MYSQL_HOST"] = "localhost"  # os.environ.get("MYSQL_HOST")
server.config["MYSQL_USER"] = "root"  # os.environ.get("MYSQL_USER")
server.config["MYSQL_PASSWORD"] = "wednesday"  # os.environ.get("MYSQL_PASSWORD")
server.config["MYSQL_DB"] = "auth"  # os.environ.get("MYSQL_DB")
server.config["MYSQL_PORT"] = 3306  # os.environ.get("MYSQL_PORT")


@server.route("/login", methods=["POST"])
def login():
    auth = request.authorization
    if not auth:
        return "missing credentials", 401

    cur = mysql.connection.cursor()
    res = cur.execute(
        "SELECT email, password FROM user WHERE email=%s", (auth.username,)
    )

    if res:
        user_row = cur.fetchone()
        email = user_row[0]
        password = user_row[1]

        if auth.username != email or auth.password != password:
            return "invalid credentials", 401
        else:
            return createJWT(auth.username, "o498738rijndfhgvt3fy78okmjhgvcxes3w4er5drew2qw3e4dt", True)
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
            encoded_jwt, "o498738rijndfhgvt3fy78okmjhgvcxes3w4er5drew2qw3e4dt", "HS256"  # os.environ.get("JWT_SECRET")
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
        algorithm="HS256",
    )


if __name__ == "__main__":
    server.run(host="0.0.0.0", port=5000)
