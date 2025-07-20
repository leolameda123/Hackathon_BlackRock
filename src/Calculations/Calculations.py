from src.DataManipulation.DataUnion import UniteSavingByDatesRanges
from datetime import datetime

def CalculateRemanents(amount):
    ceil = (amount//100 + 1) * 100
    remanent = int((ceil - amount)*100)/100
    return (float(ceil), float(remanent))

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