from src.DataModels.ReturnsResponse import ReturnsResponse
from src.DataModels.TransactionValidatorResponse import TransactionValidatorResponse
import os
from flask import Flask, request
from datetime import datetime

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY="SuperSpecialAwesomeSecretKey"
    )

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    from .Blueprints import State
    app.register_blueprint(State.bp)

    from .Blueprints import Transactions
    app.register_blueprint(Transactions.bp)
    
    from .Blueprints import Returns
    app.register_blueprint(Returns.bp)

    from .Blueprints import Performance
    app.register_blueprint(Performance.bp)

    return app

