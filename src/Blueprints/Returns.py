from flask import (Blueprint, flash, g, request)
from src.DataModels.TransactionValidatorResponse import TransactionValidatorResponse
from src.DataModels.ReturnsResponse import ReturnsResponse
from src.CoreLogic.Validator import Validator
from src.CoreLogic.Remanents import GetRemanents
from src.DataManipulation.DataUnion import UniteFixedRanges, UniteExtraRanges
from src.Calculations.Calculations import CalculateInvestedData

bp = Blueprint('returns', __name__, url_prefix='/blackrock/challenge/v1')

@bp.get('returns:<method>')
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
