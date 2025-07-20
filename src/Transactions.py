from flask import (Blueprint, flash, g, redirect, render_template, request, session, url_for)
from src.DataModels.TransactionValidatorResponse import TransactionValidatorResponse
from src.CoreLogic.Validator import Validator
from src.CoreLogic.Remanents import GetRemanents
from src.DataManipulation.DataUnion import UniteFixedRanges, UniteExtraRanges

bp = Blueprint('transactions', __name__, url_prefix='/blackrock/challenge/v1')

@bp.get('/transactions:<method>')
def Transactions(method):
    try:
        data = request.get_json()
    except:
        return "error in request"
        
    if method == "parse":

        GetRemanents(data)
        return data
    
    elif method == "validator":
        validatorResponse = TransactionValidatorResponse()
        Validator(data, validatorResponse)
        return validatorResponse.response
    
    elif method == "filter":
        
        fixedRanges = UniteFixedRanges(data["q"])
        extraRanges = UniteExtraRanges(data["p"])
        
        validatorResponse = TransactionValidatorResponse()
        Validator(data, validatorResponse, fixedRanges, extraRanges, True)

        return validatorResponse.response 

    else:
        return "error in request"# send error 300 i think XD