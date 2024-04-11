from flask import Blueprint
from flask import Flask,request,jsonify  #g 可以存储全局变量
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
from redis import Redis
from exts import db,mail,xtredis
from models.table import EmailCaptcha
import string
import random
from flask_mail import Message


bp = Blueprint('email',__name__,url_prefix="/")

@bp.route('/captcha/email',methods=['GET','POST'])
def get_email_captcha():
    email = request.args.get('email')
    source = string.digits*4
    captcha = random.sample(source,4)
    captcha = "".join(captcha)
    message = Message(subject='注册验证码',recipients=[email],body=f'您的注册验证码是:{captcha},请勿告知他人!')
    mail.send(message)
    email_captcha = EmailCaptcha(email=email,captcha=captcha)
    db.session.add(email_captcha)
    db.session.commit()
    return jsonify({'code':200,'message':'','data':None})

# # 测试用
# @bp.route('/mail')
# def send_mail():
#     try:  
#         message = Message(subject='test', recipients=['1303101041@qq.com'], body='test mail')  
#         mail.send(message)  
#         return '成功'  
#     except Exception as e:  
#         return f'邮件发送失败:6 {e}'