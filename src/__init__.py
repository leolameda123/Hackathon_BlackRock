import os
from flask import Flask, request

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

    @app.get('/blackrock/challenge/v1/transactions:parse')
    def ParseTransactions():
        data = request.get_json()
        GetRemanents(data)
        return data
        
    return app

    @app.get('/blackrock/challenge/v1/transactions:validator')
    def ParseTransactions():
        data = request.get_json()
        return Validator(data)
        
    return app

def GetRemanents(data):
    for entry in data:
        amount = entry["amount"]
        if amount > 0:
            entry["amount"] = float(amount)
            entry["ceiling"], entry["remanent"] = CalculateRemanents(amount)

        else:
            entry["ceiling"] = 0
            entry["remanent"] = 0
    return

def CalculateRemanents(amount):
    ceil = (amount//100 + 1) * 100
    remanent = int((ceil - amount)*100)/100
    return (float(ceil), float(remanent))

def Validator(data):
    hs = set()
    valid = []
    invalid = []

    wage = data["wage"]
    transactions = data["transactions"]

    for entry in transactions:
        temp = (entry["date"], entry["amount"], entry["ceiling"], entry["remanent"])
        hs.append(temp)
        if DuplicateValidator != True:
            invalid.append(entry)
            continue
        if ZeroValidator != True:
            invalid.append(entry)
            continue
        if PositiveValidator != True:
            invalid.append(entry)
            continue
        if RemanentValidator != True:
            invalid.append(entry)
            continue
        
        valid.append(entry)

    return {"valid": valid, "invalid": invalid} 



def DuplicateValidator(entry, hs):
    return True if entry not in hs else "Duplicate Transaction"

def ZeroValidator(entry):
    return True if entry["amount"] != 0 else "Zero amounts are not allowed"

def PositiveValidator(entry):
    return True if entry["amount"] > 0 else "Negative amounts are not allowed"

def RemanentValidator(entry):
    return True if (entry["ceiling"], entry["remanent"]) == CalculateRemanents(entry["amount"]) else "Error in remanent values"
