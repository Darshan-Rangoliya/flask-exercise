from flask import Flask,redirect,render_template,Blueprint,request
from .models import UserModel,db

bp = Blueprint('auth',__name__)

@bp.post('/user')
def user():
    if request.is_json:
        data = request.get_json()
        new_user = UserModel(username=data['username'],password=data['password'])
        db.session.add(new_user)
        db.session.commit()
        return {'message':'data added successfully'}