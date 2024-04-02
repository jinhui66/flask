from flask import Blueprint,url_for
from flask_mail import Message
from flask import request,render_template,session,redirect
from exts import db,mail
from models.table import User, Resume, Position, Comment, Send_resume, Admin
import os

# admin
bp = Blueprint('admin',__name__,url_prefix="/")

@bp.route('/recruit',methods=['GET','POST'])
def recruit():
    if request.method == 'GET':
        # 显示已发布的招聘
        admin_id = session.get('user_id')
        results_data = Position.query.filter_by(admin_id=admin_id)
        released_positions = []
        for result in results_data:
            released_positions.append({
            "id": result.id,
            "company": result.company,
            "position_name": result.position_name,
            "salary": result.salary,
            "education": result.education,
            "description": result.description,
            "address": result.address,
            "release_time":result.release_time,
            "public":result.public,
            "admin":result.admin
            })
        return render_template('admin/recruit.html',released_positions=released_positions)
    else:
        pass
        # admin_id = session.get('user_id')
        # return render_template('admin/recruit.html')
    
@bp.route('/recruit_info',methods=['GET','POST'])
def recruit_info():
    if request.method == 'GET':
        # admin_id = session.get('user_id')
        position_id = request.args.get('position_id')
        receive_resumes = Send_resume.query.filter_by(position_id=position_id).all()
        resumes = []
        for receive_resume in receive_resumes:
            resumes.append(receive_resume)
        return render_template('admin/recruit_info.html',resumes=resumes)                
    else:
        # admin_id = session.get('user_id')
        position_id = request.form.get('position_id')
        receive_resumes = Send_resume.query.filter_by(position_id=position_id).all()
        resumes = []
        for receive_resume in receive_resumes:
            resumes.append(receive_resume)
        return render_template('admin/recruit_info.html',resumes=resumes)
    
@bp.route('/recruit_release',methods=['GET','POST'])
def recruit_release():
    if request.method == 'GET':
        return render_template('admin/recruit_release.html')
    else:
        return render_template('admin/recruit_release.html')
    
@bp.route('/release_action',methods=['GET','POST'])
def release_action():
    if request.method == 'GET':
        pass
    else:
        admin_id = session.get('user_id')
        company = request.form.get('company')
        position_name = request.form.get('position_name')
        salary = request.form.get('salary')
        education = request.form.get('education')
        address = request.form.get('address')
        description = request.form.get('description')
        
        position = Position()
        position.company = company
        position.position_name = position_name
        position.salary = salary
        position.education = education
        position.address = address
        position.description = description
        position.admin_id = admin_id
        
        db.session.add(position)
        db.session.commit()
        
        if not os.path.exists(f'data/send_resumes/{position.id}'):
            os.mkdir(f'data/send_resumes/{position.id}')

        return redirect(url_for("admin.recruit",method='POST'))
        
@bp.route('/stop_recruit',methods=['GET','POST'])
def stop_recruit():
    if request.method == 'GET':
        pass
    else:
        position_id = request.form.get('position_id')
        position = Position.query.filter_by(id=position_id).first()
        print(position_id)
        position.public = 0
        db.session.commit()
        return redirect(url_for("admin.recruit"))
    
