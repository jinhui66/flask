from flask import Blueprint
from flask import request,flash,session,redirect,url_for,send_file   #g 可以存储全局变量
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
from redis import Redis
from exts import db,mail,xtredis
import os
from models.table import Resume
from werkzeug.utils import secure_filename  
from models.function import extract_text_from_pdf
from models.table import User, Admin

bp = Blueprint('load',__name__,url_prefix="/")

@bp.route('/upload',methods=['GET','POST'])
def upload_pdf():
    file = request.files['file_name']  
    if file.filename == '':  
        flash('No selected file')  
        return redirect(url_for('user.resume'))  
    if file:  
        user_id = session.get('user_id')
        resume = Resume.query.filter_by(user_id=user_id).first()
        # filename = secure_filename(file.filename) 
        resume.filepath = str(user_id)+'/'+'resume.pdf'
        root_path = 'static/resumes/'+resume.filepath
        file.save(root_path)  
        db.session.commit()
        print(extract_text_from_pdf(root_path))
        flash('File successfully uploaded')  
        return redirect(url_for('user.resume'))  
    return redirect(url_for('user.resume'))  
    
@bp.route('/upload_pic',methods=['GET','POST'])
def upload_pic():
    file = request.files['file_name']  
    if file.filename == '':  
        flash('No selected file')  
        return redirect(url_for('user.user_info'))  
    if file:  
        user_id = session.get('user_id')
        type = session['type']
        if type == 'user':
            user = User.query.filter_by(id=user_id).first()
        else:
            user = Admin.query.filter_by(id=user_id).first()
        filename = secure_filename(file.filename) 
        user.filepath = str(user_id)+'/'+'picture.jpg'
        root_path = f'static/pictures/{type}/' + user.filepath
        file.save(root_path)  
        db.session.commit()
        # print(extract_text_from_pdf(resume.filepath))
        flash('File successfully uploaded')  
        return redirect(url_for('user.user_info'))  
    return redirect(url_for('user.resume'))  