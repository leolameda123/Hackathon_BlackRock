import os
from flask import Flask, request
from collections import OrderedDict

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY="SuperSpecialAwesomeSecretKey"
    )

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    @app.route("/")
    def test():
        return "I'm Alive"

    @app.post('/blackrock/challenge/v1/transactions:parse')
    def ParseTransactions():
        data = request.get_json()
        GetRemanents(data["Gastos"])
        return data
        
    return app

def GetRemanents(data):
    for entry in data:
        amount = entry["amount"]
        ceil = (amount//100 + 1) * 100
        remanent = int((ceil - amount)*100)/100

        entry["amount"] = float(amount)
        entry["ceiling"] = float(ceil)
        entry["remanent"] = remanent
    return