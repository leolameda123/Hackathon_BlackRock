from flask import (Blueprint, g, request)
import time

bp = Blueprint("performance", __name__, url_prefix="/blackrock/challenge/v1")

@bp.get("/performance")
def State():
    return "Hello There"

@bp.before_request
def getStartTime():
    
    g.startTime = time.time()
    print(startTime)
    return

@bp.after_request
def getEndTime(response):

    endTime = time.time()
    print(endTime - g.endTime)
    return response