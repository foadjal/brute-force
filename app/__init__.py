from flask import Flask

def create_app():
    app = Flask(__name__)
    app.secret_key = "super-secret-key"  # à changer plus tard
    from .routes import main
    app.register_blueprint(main)
    return app
