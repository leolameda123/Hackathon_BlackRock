from flask import (Blueprint, g)

bp = Blueprint("state", __name__, url_prefix="/blackrock/challenge/v1")

@bp.get("/state")
def State():
    return {"status": "I'm Alive"}