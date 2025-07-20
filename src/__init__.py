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

    @app.get('/blackrock/challenge/v1/returns:<method>')
    def Returns(method):
        try:
            data = request.get_json()
        except:
            return "error in request"

        returnResponse = ReturnsResponse()
            
        fixedRanges = UniteFixedRanges(data["q"])
        extraRanges = UniteExtraRanges(data["p"])

        validatorResponse = TransactionValidatorResponse()

        returnResponse.response["transactionsTotalAmount"], returnResponse.response["transactionsTotalCeiling"] = Validator(data, validatorResponse, fixedRanges, extraRanges, True)

        interes = 7.11 if method == "ppr" else 14.49

        CalculateInvestedData(returnResponse.response, method, interes, 
                            data, validatorResponse.response["valid"])
        
        return returnResponse.response

    from . import State
    app.register_blueprint(State.bp)

    from . import Transactions
    app.register_blueprint(Transactions.bp)
    

    return app

##########################

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

def Validator(data, res, fixedRanges=None, extraRanges=None, updateRemanent = False):

    hs = set()
    transactionsTotalAmount = 0
    transactionsTotalCeiling = 0

    for entry in data["transactions"]:

        temp = (entry["date"], entry["amount"], entry["ceiling"], entry["remanent"])
        
        duplicate = DuplicateValidator(temp, hs)
        if duplicate is not True:
            entry["message"] = duplicate
            res.response["invalid"].append(entry)
            continue
        
        hs.add(temp)
        
        zeroAmount = ZeroAmoutValidator(entry)
        if zeroAmount is not True:
            entry["message"] = zeroAmount
            res.response["invalid"].append(entry)
            continue

        positiveAmount = PositiveValidator(entry)
        if positiveAmount is not True:
            entry["message"] = positiveAmount
            res.response["invalid"].append(entry)
            continue
        
        remanentCorrect = RemanentValidator(entry)
        if remanentCorrect is not True:
            entry["message"] = remanentCorrect
            res.response["invalid"].append(entry)
            continue

        transactionsTotalAmount += entry["amount"]
        transactionsTotalCeiling += entry["remanent"]

        if updateRemanent:

            entryDate = datetime.strptime(entry["date"], "%Y-%m-%d %H:%M")

            fixed = [x for x in fixedRanges 
                    if any([True for start, end in fixedRanges[x]
                    if start <= entryDate <= end])]
            
            extra = [x for x in extraRanges 
                        if any([True for start, end in extraRanges[x]
                        if start <= entryDate <= end])]
            
            if fixed:

                entry["updatedRemanent"] = min(fixed)
                zeroAmount = ZeroRemanentValidator(entry)

                if zeroAmount is not True:
                    entry["message"] = zeroAmount
                    res.response["invalid"].append(entry)
                    continue

            elif extra:

                if extra:
                    entry["updatedRemanent"] = entry["remanent"] + min(extra)
                
            else:
                entry["updatedRemanent"] = entry["remanent"]

        res.response["valid"].append(entry)


    return (transactionsTotalAmount, transactionsTotalCeiling)

def DuplicateValidator(entry, hs):
    return True if entry not in hs else "Duplicate Transaction"

def ZeroAmoutValidator(entry):
    return True if entry["amount"] != 0 else "Zero amounts are not allowed"

def ZeroRemanentValidator(entry):
    return True if entry["updatedRemanent"] != 0 else "Zero Remanents are not allowed"

def PositiveValidator(entry):
    return True if entry["amount"] > 0 else "Negative amounts are not allowed"

def RemanentValidator(entry):
    return True if (entry["ceiling"], entry["remanent"]) == CalculateRemanents(entry["amount"]) else "Error in transaction values"

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

def UniteSavingByDatesRanges(ranges):

    savingsByDatesRanges = []

    for entry in ranges:
        start = datetime.strptime(entry["start"], "%Y-%m-%d %H:%M")
        end = datetime.strptime(entry["end"], "%Y-%m-%d %H:%M")
        savingsByDatesRanges.append((start, end))
        entry["amount"] = 0

    return savingsByDatesRanges

#################

def CalculateInvestedData(res, investmentType, interest, data, transactions):

    savingsByDatesRanges = UniteSavingByDatesRanges(data["k"])
    
    for entry in transactions:
        res["investedAmount"] += entry["updatedRemanent"]
        CalculateSavingsByDate(savingsByDatesRanges, data["k"], entry)

    userAge = data["age"]
    inflation = data["inflation"]
    P = res["investedAmount"]
    t = 65 - (userAge+1) if userAge < 65 else 5
    Ai = int((P * (1 + (interest/100))**t)*100)/100

    if investmentType == "ppr":
        wage = data["wage"]
        payback = P if P < wage/100 else wage/100
        Ai += payback*t

    print(Ai)

    Af = Ai/(1+ (inflation/100))**t
    res["profits"] = int(Af*100)/100
    res["savingsByDates"] = data["k"]

    return 

def CalculateSavingsByDate(savingsByDatesRanges, savingsByDates, entry):

    transactionDate = datetime.strptime(entry["date"], "%Y-%m-%d %H:%M")
    for i, (start, end) in enumerate(savingsByDatesRanges):
        if start <= transactionDate <= end:
            savingsByDates[i]["amount"] += entry["updatedRemanent"]

    return