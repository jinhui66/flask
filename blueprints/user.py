from flask import Blueprint,url_for
from flask_mail import Message
from flask import request,render_template,session,redirect
from exts import db,mail
from models.table import User, Resume, Position, Comment, Send_resume, Admin
from models.forms import ChangeForm
import os
import shutil
import base64

# user
bp = Blueprint('user',__name__,url_prefix="/")

@bp.route('/resume',methods=['GET','POST'])
def resume():
    if request.method == 'GET':
        if session:
            user_id = session.get('user_id')
            resume = Resume.query.filter_by(user_id=user_id).first()
            resume.phone = base64.b64decode(resume.phone.encode('utf-8')).decode('utf-8')
            resume.email = base64.b64decode(resume.email.encode('utf-8')).decode('utf-8')
            print(resume.email)
            user = User.query.filter_by(id=session['user_id']).first()
            return render_template('menu/resume.html',resume=resume)
        else:
            return redirect('../login')
    else: # 'POST'
        user_id = session.get('user_id')
        user = User.query.filter_by(id=user_id).first()
        name = request.form.get('name')
        age = request.form.get('age')
        gender = request.form.get('gender')
        expect_position = request.form.get('expect_position')
        marriage = request.form.get('marriage')
        phone = request.form.get('phone')
        expect_salary = request.form.get('expect_salary')
        email = request.form.get('email')
        expect_address = request.form.get('expect_address')
        education = request.form.get('education')
        experience = request.form.get('experience')
        abilities = request.form.get('abilities')
        about_me = request.form.get('about_me')

        # 检查空值并设置默认值   
        if not age or not age.isdigit():  
            age = 0  
        if not expect_salary or not expect_salary.isdigit():  
            expect_salary = 0  
        
        resume = Resume.query.filter_by(user_id=user.id).first()
        
        if resume:
            resume.name = name  
            resume.age = age  
            resume.gender = gender  
            resume.expect_position = expect_position
            resume.marriage = marriage
            resume.phone = base64.b64encode(phone.encode('utf-8'))
            resume.expect_salary = expect_salary
            resume.email = base64.b64encode(email.encode('utf-8'))
            resume.expect_address = expect_address
            resume.education = education
            resume.experience = experience
            resume.abilities = abilities
            resume.about_me = about_me
        # 提交
            db.session.commit()
            resume.phone = base64.b64decode(resume.phone.encode('utf-8')).decode('utf-8')
            resume.email = base64.b64decode(resume.email.encode('utf-8')).decode('utf-8')
            return render_template('menu/resume.html',resume=resume)
        else:
            return('失败')
    
        
@bp.route('/user_info',methods=['POST','GET'])
def user_info():
    error=''
    if request.method=='GET':
        pass
    else:
        username = request.form.get('username')
        user_id = session.get('user_id')
        if session['type'] == 'user':
            user = User.query.filter_by(id=user_id).first()
        else:
            user = Admin.query.filter_by(id=user_id).first()
        form = ChangeForm(request.form)
        if form.validate():
            username = form.username.data
            user.username = username
            db.session.commit()
            return render_template('menu/user_info.html')
        elif user.username==username:
            return render_template('menu/user_info.html')
        else:
            for field, errors in form.errors.items():  
                # errors 是一个列表，包含该字段的所有错误消息  
                if errors:  
                #     # 打印第一个错误消息  
                    error = errors[0]
                    print(f"{field} 的第一个错误是: {errors[0]}")  
                    break
                print(error)
            return render_template('menu/user_info.html',error=error)
    return render_template('menu/user_info.html')

@bp.route('/send_resume',methods=['POST','GET'])
def send_resume():
    if request.method == 'POST':
        user_id = session.get('user_id')
        position_id = request.form.get('position_id')
        resume = Resume.query.filter_by(user_id=user_id).first()
        
        if not os.path.exists(f'data/send_resumes/{position_id}/{user_id}'):
            os.mkdir(f'data/send_resumes/{position_id}/{user_id}')
        
        if resume.filepath == '' or not os.path.exists(f'data/resumes/{resume.filepath}'):
            return '请上传简历'
            
        filepath = f'data/send_resumes/{position_id}/' + resume.filepath
        shutil.copy(f'data/resumes/{resume.filepath}',filepath)
        
        
        
        if Send_resume.query.filter_by(user_id=user_id,position_id=position_id).first() is not None :
            send = Send_resume.query.filter_by(user_id=user_id,position_id=position_id).first()
            send.name = resume.name  
            send.age = resume.age  
            send.gender = resume.gender  
            send.expect_position = resume.expect_position
            send.marriage = resume.marriage
            send.phone = resume.phone
            send.expect_salary =resume. expect_salary
            send.email = resume.email
            send.expect_address = resume.expect_address
            send.education = resume.education
            send.experience = resume.experience
            send.abilities = resume.abilities
            send.about_me = resume.about_me
            send.filepath = resume.filepath
            send.status = 'waiting'
            
        else:
            send = Send_resume(name = resume.name,
                            age = resume.age,
                            expect_position = resume.expect_position,
                            gender = resume.gender,
                            marriage = resume.marriage,
                            phone = resume.phone,
                            expect_salary = resume.expect_salary,
                            email = resume.email,
                            expect_address = resume.expect_address,
                            education = resume.education,
                            experience = resume.experience,
                            abilities = resume.abilities,
                            about_me = resume.about_me,
                            user_id = user_id,
                            position_id = position_id,
                            filepath = resume.filepath,
                            status = 'waiting'
                            )

            db.session.add(send)
        db.session.commit()
        
    return redirect(url_for('menu.menu'))

# 查看已投简历
@bp.route('/sended_resume')
def sended_resume():
    if request.method == 'POST':
        user_id = session.get('user_id')
        pass
    else:
        user_id = session.get('user_id')
        resumes = Send_resume.query.filter_by(user_id=user_id).all()
        sended_resumes = []
        for send_resume in resumes:
            sended_resumes.append(send_resume)
        return render_template('menu/sended_resume.html',sended_resumes=sended_resumes)