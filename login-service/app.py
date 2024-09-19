from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
import psycopg2

if __name__ == '__main__':
    app = Flask(__name__)

    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://admin:password@login-database:5432/logindb'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db = SQLAlchemy(app)

    import routes

    app.run(host='0.0.0.0', port=5000)