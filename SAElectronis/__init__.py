from flask import Flask, render_template, request, session
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()
app=Flask(__name__)
def create_app():
    
    app.debug=True

    app.secret_key = 'AniketIsRude'

    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///milton.sqlite'
    
    db.init_app(app)
    


    from . import views
    app.register_blueprint(views.bp)

    return app
