from flask import (Blueprint, g, request)
from datetime import datetime
from src.DB.db import postData, retrieveData, updateData
from src.DataModels.PerformanceResponse import PerformanceResponse
import os
import psutil
import threading

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
    time = f"{str(g.startTime)[:10]} {str(elapsedTime)}"

    process = psutil.Process(os.getpid())
    ram_used = (process.memory_info().rss / (1024 * 1024))*1000 
    updateData(time, request.path, round(ram_used, 2), len(threading.enumerate()))

    return response

@bp.get("/performance")
def performance():
    performanceResponse = PerformanceResponse()

    data = retrieveData()
    performanceResponse.response["time"] = data["elapsedTime"]
    performanceResponse.response["memory"] = data["memory"]
    performanceResponse.response["threads"] = data["threads"]
    
    return performanceResponse.response
