from datetime import datetime

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
