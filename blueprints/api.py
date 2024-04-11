from flask import Blueprint
from flask import request,flash,session,redirect,url_for,send_file   #g 可以存储全局变量
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
from redis import Redis
import openai

bp = Blueprint('api',__name__,url_prefix="/")

@bp.route('/chat_api',methods=['GET','POST'])
def chat_api():
    openai.api_key = key