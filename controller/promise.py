from flask import Blueprint

bp = Blueprint('promise', __name__, url_prefix='/promise')

@bp.route('/summary')
def summary():
    return "summary"