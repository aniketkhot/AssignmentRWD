from flask import Flask, render_template


app=Flask(__name__)
def create_app():
    
    app.debug=True
    
    from . import views
    app.register_blueprint(views.bp)

    return app
