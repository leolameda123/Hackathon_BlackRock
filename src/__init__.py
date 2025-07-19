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

    @app.get('/blackrock/challenge/v1/transactions:<data>')
    def ParseTransactions(data):
        if data == "parse":
            data = request.get_json()
            GetRemanents(data)
            return data
        elif data == "validator":
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

    for entry in data["transactions"]:

        temp = (entry["date"], entry["amount"], entry["ceiling"], entry["remanent"])
        
        duplicate = DuplicateValidator(temp, hs)
        if duplicate is not True:
            entry["message"] = duplicate
            invalid.append(entry)
            continue
        
        zeroAmount = ZeroValidator(entry)
        if zeroAmount is not True:
            invalid.append(entry)
            continue
        
        positiveAmount = PositiveValidator(entry)
        if positiveAmount is not True:
            invalid.append(entry)
            continue
        
        remanentCorrect = RemanentValidator(entry)
        if remanentCorrect is not True:
            invalid.append(entry)
            continue

        hs.add(temp)
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
