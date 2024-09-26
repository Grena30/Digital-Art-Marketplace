from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_jwt_extended import JWTManager
from datetime import timedelta


ACCESS_EXPIRES = timedelta(minutes=15)

if __name__ == '__main__':
    app = Flask(__name__)

    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://admin:password@art-database:5432/artdb'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config["JWT_SECRET_KEY"] = "super-secret"
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = ACCESS_EXPIRES
    jwt = JWTManager(app)
    db = SQLAlchemy(app)

    limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["200 per day", "50 per hour", "15 per minute"]
    )

    import routes

    app.run(host='0.0.0.0', port=5001)