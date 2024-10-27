from flask import Flask, render_template, request, session


app=Flask(__name__)
def create_app():
    
    app.debug=True

    app.secret_key = 'AniketIsRude'
    
    from . import views
    app.register_blueprint(views.bp)

    return app
