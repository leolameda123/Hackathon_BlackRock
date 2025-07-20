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

            return Validator(data, fixedRanges, extraRanges, True)

        else:
            return "error in request"# send error 300 i think XD

    @app.get('/blackrock/challenge/v1/returns:<method>')
    def Returns(method):
        try:
            data = request.get_json()
        except:
            return "error in request"

        res = {
            "transactionsTotalAmount": 0,
            "transactionsTotalCeiling": 0,
            "investedAmount": 0,
            "profits": 0,
            "savingsByDates":[]
        }
            
        if method == "ppr":

            fixedRanges = UniteFixedRanges(data["q"])
            extraRanges = UniteExtraRanges(data["p"])

            validTransactions = Validator(data)["valid"]
            UpdateRemanent(fixedRanges, extraRanges, validTransactions)

            res["profits"] = CalculateInvestedData(res, method, data["inflation"], 7.11, 
                            data["age"], validTransactions, data["wage"])
            
            CalculateSavingsByDate(res, data["k"], validTransactions)
            return res
        
        elif method == "ishares": 

            fixedRanges = UniteFixedRanges(data["q"])
            extraRanges = UniteExtraRanges(data["p"])

            validTransactions = Validator(data)["valid"]
            UpdateRemanent(fixedRanges, extraRanges, validTransactions)

            res["profit"] = CalculateInvestedData(res, method, data["inflation"], 14.49, 
                            data["age"], validTransactions)
            
            CalculateSavingsByDate(res, data["k"], validTransactions)
            return res

        else:
            return "error in request"# send error 300 i think XD

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

def Validator(data, fixedRanges=None, extraRanges=None, updateRemanent = False):
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
        
        hs.add(temp)
        
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

        if updateRemanent:

            entryDate = datetime.strptime(entry["date"], "%Y-%m-%d %H:%M")
            fixedModifier = None

            if fixedRanges:

                fixed = [x for x in fixedRanges 
                        if any([True for start, end in fixedRanges[x]
                        if start <= entryDate <= end])]
                
                if fixed:
                    fixedModifier = min(fixed)
                    entry["remanent"] = fixedModifier

            if extraRanges and fixedModifier is None:
                extra = [x for x in extraRanges 
                        if any([True for start, end in extraRanges[x]
                        if start <= entryDate <= end])]

                if extra:
                    extraModifier = min(extra)
                    entry["remanent"] += extraModifier

        zeroAmount = ZeroValidator(entry)
        if zeroAmount is not True:
            entry["message"] = zeroAmount
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

#################

def CalculateInvestedData(res, investmentType, inflation, interest, userAge, data, wage=0):
    
    for entry in data:
        res["transactionsTotalAmount"] += entry["amount"]
        res["transactionsTotalCeiling"] += entry["remanent"]
        res["investedAmount"] += entry["updated_remanent"]

    P = res["investedAmount"]
    t = 65 - (userAge+1) if userAge < 65 else 5
    Ai = P * (1 + (interest/100))**t

    if investmentType == "ppr":
        payback = res["investedAmount"] if res["investedAmount"] < wage/100 else wage/100
        Ai += payback*t

    print(Ai)

    Af = Ai/(1+ (inflation/100))**t
    
    return int(Af*100)/100

def CalculateSavingsByDate(res, data, transactions):

    savingsByDatesRanges = []
    for entry in data:
        start = datetime.strptime(entry["start"], "%Y-%m-%d %H:%M")
        end = datetime.strptime(entry["end"], "%Y-%m-%d %H:%M")
        savingsByDatesRanges.append((start, end))

    amounts = [0]*len(savingsByDatesRanges)
    for transaction in transactions:
        transactionDate = datetime.strptime(transaction["date"], "%Y-%m-%d %H:%M")
        for i, (start, end) in enumerate(savingsByDatesRanges):
            if start <= transactionDate <= end:
                amounts[i] += transaction["updated_remanent"]
    
    res["savingsByDates"] = data
    for i, entry in enumerate(data):
        entry["amount"] = amounts[i]