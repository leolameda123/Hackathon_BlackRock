from datetime import datetime

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
