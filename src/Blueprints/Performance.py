from flask import (Blueprint, g, request)
from datetime import datetime
from src.DB.db import postData, retrieveData, updateData

bp = Blueprint("performance", __name__, url_prefix="/blackrock/challenge/v1")

@bp.before_app_request
def getStartTime():

    if request.path == "/blackrock/challenge/v1/performance":
        return

    g.startTime = datetime.now()
    return

@bp.after_app_request
def getEndTime(response):
    
    if request.path == "/blackrock/challenge/v1/performance":
        return response

    elapsedTime = datetime.now() - g.startTime
    print(g.startTime, elapsedTime, request.path)

    time = f"{str(g.startTime)[:10]} {str(elapsedTime)}"
    updateData(time, request.path)

    return response

@bp.get("/performance")
def performance():

    timer = retrieveData()
    print(timer["elapsedTime"], timer["lastEndpointUsed"])

    return "x"
