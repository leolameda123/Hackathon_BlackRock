import os
from flask import Flask, request, g
from datetime import datetime
from src.DataModels.ReturnsResponse import ReturnsResponse
from src.DataModels.TransactionValidatorResponse import TransactionValidatorResponse

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY="SuperSpecialAwesomeSecretKey",
        DATABASE=os.path.join(app.instance_path, 'flask.sqlite')
    )

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    from .DB import db
    db.init_app(app)

    from .Blueprints import State
    app.register_blueprint(State.bp)

    from .Blueprints import Transactions
    app.register_blueprint(Transactions.bp)
    
    from .Blueprints import Returns
    app.register_blueprint(Returns.bp)

    from .Blueprints import Performance
    app.register_blueprint(Performance.bp)
    
    return app

