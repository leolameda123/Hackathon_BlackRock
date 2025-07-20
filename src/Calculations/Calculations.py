def CalculateRemanents(amount):
    ceil = (amount//100 + 1) * 100
    remanent = int((ceil - amount)*100)/100
    return (float(ceil), float(remanent))