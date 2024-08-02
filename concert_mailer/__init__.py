
import os
from flask import Flask
from flask_mail import Mail

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'concert_mailer.sqlite'),
    )

    app.config.update(
    MAIL_SERVER='smtp.example.com',
    MAIL_PORT=587,
    MAIL_USE_TLS=True,
    MAIL_USERNAME='coleparksphotography@gmail.com',
    MAIL_PASSWORD='6JAT4-8X00H-L7MFN-94T68-4NG5P1'
    )
    mail = Mail(app)

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass


    # a simple page that says hello
    @app.route('/hello')
    def hello():
        return 'Hello, World!'

    
    from . import db
    db.init_app(app)

    from . import auth
    app.register_blueprint(auth.bp)

    from . import concert
    app.register_blueprint(concert.bp)
    app.add_url_rule('/', endpoint='index')


    return app