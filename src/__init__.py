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

    @app.route("/blackrock/challenge/v1/state")
    def State():
        return "I'm Alive"

    @app.get('/blackrock/challenge/v1/transactions:<method>')
    def Transactions(method):
        try:
            data = request.get_json()
        except:
            return "error in request"
            
        if method == "parse":

            GetRemanents(data)
            return data
        
        elif method == "validator":

            return Validator(data)
        
        elif method == "filter":
            
            fixedRanges = UniteFixedRanges(data["q"])
            extraRanges = UniteExtraRanges(data["p"])

            print(len(fixedRanges[0]), fixedRanges)
            print(len(extraRanges[25]), extraRanges)

            UpdateRemanent(fixedRanges, extraRanges, data["transactions"])

            return Validator(data)

        else:
            return "error in request"# send error 300 i think XD

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

############################

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
            entry["message"] = zeroAmount
            invalid.append(entry)
            continue
        
        positiveAmount = PositiveValidator(entry)
        if positiveAmount is not True:
            entry["message"] = positiveAmount
            invalid.append(entry)
            continue
        
        remanentCorrect = RemanentValidator(entry)
        if remanentCorrect is not True:
            entry["message"] = remanentCorrect
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

############################

def UniteFixedRanges(ranges):

    unitedFixedRanges = dict()

    for entry in ranges:
        
        if entry["fixed"] in unitedFixedRanges:
            unitedFixedRanges[entry["fixed"]].append((datetime.strptime(entry["start"], "%Y-%m-%d %H:%M"), datetime.strptime(entry["end"], "%Y-%m-%d %H:%M")))
        
        else:
            unitedFixedRanges[entry["fixed"]] = [(datetime.strptime(entry["start"], "%Y-%m-%d %H:%M"), datetime.strptime(entry["end"], "%Y-%m-%d %H:%M"))]
    
    return unitedFixedRanges

def UniteExtraRanges(ranges):

    unitedExtraRanges = dict()

    for entry in ranges:
        
        if entry["extra"] in unitedExtraRanges:
            unitedExtraRanges[entry["extra"]].append((datetime.strptime(entry["start"], "%Y-%m-%d %H:%M"), datetime.strptime(entry["end"], "%Y-%m-%d %H:%M")))
        
        else:
            unitedExtraRanges[entry["extra"]] = [(datetime.strptime(entry["start"], "%Y-%m-%d %H:%M"), datetime.strptime(entry["end"], "%Y-%m-%d %H:%M"))]
    
    return unitedExtraRanges

def UpdateRemanent(fixedRanges, extraRanges, data):

    for entry in data:
        
        modifiers = [entry["remanent"], 0]
        entryDate = datetime.strptime(entry["date"], "%Y-%m-%d %H:%M")

        fixed = [x for x in fixedRanges 
                if any([True for start, end in fixedRanges[x]
                if start <= entryDate <= end])]

        extra = [x for x in extraRanges 
                if any([True for start, end in extraRanges[x]
                if start <= entryDate <= end])]

        print(fixed, extra)
        if fixed:
            modifiers[0] = min(fixed)
        if extra:
            modifiers[1] = min(extra)
        
        entry["updated_remanent"] = sum(modifiers)
    
    return
