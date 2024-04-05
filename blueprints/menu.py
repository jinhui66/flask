from flask import Blueprint
from flask import Flask,request,render_template,session,redirect,url_for,jsonify   #g 可以存储全局变量
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
from redis import Redis
from exts import db,mail,xtredis
from models.table import User, Resume, Position, Comment, Admin
import hashlib
import json
from models.forms import RegisterForm,LoginForm,ForgotForm
from models.function import get_total_pages, redis_search_positions
import base64
import os

bp = Blueprint('menu',__name__,url_prefix="/")

@bp.route('/login',methods=['GET','POST'])
def login():
    if request.method=='GET':
        return render_template('login.html')
    if request.method=='POST':
        pass
    
@bp.route('/login_action',methods=['GET','POST'])
def login_action():
    if request.method == 'GET':
        pass
    else:
        type = request.form.get('type')
        form = LoginForm(request.form)
        if form.validate():
            email = form.email.data
            password = form.password.data
            if type == 'user':
                get_user = User.query.filter_by(email=email).first()
                if get_user is not None:
                    session['user_id'] = get_user.id
                    session['type'] = 'user'
                    password = hashlib.sha256(password.encode('utf-8')).hexdigest()
                    print(password)
                    if(get_user.password == password):
                        print(1)
                        return jsonify({'status':'success', 'message':''})
                        
            else:
                print('admin')
                get_admin = Admin.query.filter_by(email=email).first()
                if get_admin is not None:
                    session['user_id'] = get_admin.id
                    session['type'] = 'admin'
                    password = hashlib.sha256(password.encode('utf-8')).hexdigest()
                    if(get_admin.password == password):
                        return jsonify({'status': 'success', 'message':''})
        return jsonify({'status':'', 'message':'账号或密码错误'})

@bp.route('/register',methods=['GET','POST'])
def register():
    error=None
    if request.method == 'GET':
        return render_template('register.html')
    else:
        type = request.form.get('type')
        form = RegisterForm(request.form)
        if form.validate():
            email = form.email.data
            username = form.username.data
            password = form.password.data
            if type == 'user':
                user = User(email=email,username=username,password=hashlib.sha256(password.encode('utf-8')).hexdigest())
                # 创建 resume 对象并关联到 User
                resume = Resume(name ='',
                            age = 0,
                            expect_position = '',
                            gender = '',
                            marriage = '',
                            phone = '',
                            expect_salary = 0,
                            email = '',
                            expect_address = '',
                            education = '',
                            experience = '',
                            abilities = '',
                            about_me = '',
                            filepath = '')
                user.resume.append(resume)
                # 提交
                db.session.add(user)
                db.session.commit()
                # 创建文件夹
                if not os.path.exists('data/pictures/user/'+str(user.id)):  
                    os.makedirs('data/pictures/user/'+str(user.id))  
                if not os.path.exists('data/resumes/'+str(user.id)):  
                    os.makedirs('data/resumes/'+str(user.id))  
                
                return redirect(url_for('menu.login'))
            else: #type == 'admin'
                admin = Admin(email=email,username=username,password=hashlib.sha256(password.encode('utf-8')).hexdigest())
                db.session.add(admin)
                db.session.commit()
                if not os.path.exists('data/pictures/admin/'+str(admin.id)):  
                    os.makedirs('data/pictures/admin/'+str(admin.id))  
                return redirect(url_for('menu.login'))
        else:
            for field, errors in form.errors.items():  
                # errors 是一个列表，包含该字段的所有错误消息  
                if errors:  
                #     # 打印第一个错误消息  
                    error = errors[0]
                    print(f"{field} 的第一个错误是: {errors[0]}")  
                    break
                print(error)
            return render_template('register.html',error=error)

@bp.route('/forgot_password',methods=['GET','POST'])
def forgot_password():
    if request.method == 'GET':
        return render_template('forgot_password.html')
    else:
        form = ForgotForm(request.form)
        if form.validate():
            email = form.email.data
            password = form.password.data
            if User.query.filter_by(email=email).first():
                get_user = User.query.filter_by(email=email).first()
                get_user.password = hashlib.sha256(password.encode('utf-8')).hexdigest()
            elif Admin.query.filter_by(email=email).first():
                get_user = Admin.query.filter_by(email=email).first()
                get_user.password = hashlib.sha256(password.encode('utf-8')).hexdigest()
            db.session.commit()
            session.clear()
            return redirect(url_for('menu.login'))
        else:
            for field, errors in form.errors.items():  
                # errors 是一个列表，包含该字段的所有错误消息  
                if errors:  
                #     # 打印第一个错误消息  
                    error = errors[0]
                    print(f"{field} 的第一个错误是: {errors[0]}")  
                    break
                print(error)
            return render_template('forgot_password.html',error=error)

@bp.route('/',methods=['GET','POST'])
def menu():
    if request.method == 'POST':
        keyword = ''
        get_user = User.query.filter_by(id=session['user_id']).first()
        results = redis_search_positions(keyword,Position)
        results_per_page = 6  # 每页显示6条结果  
        page = int(request.form.get('page', 1))  # 获取当前页码，默认为1 
        page_results, total_pages = get_total_pages(results,results_per_page,page)
        
        return render_template('index.html',user=get_user,results=page_results,total_pages=total_pages,page=page) 
    if request.method == 'GET':
        keyword = request.args.get('keyword')

        if keyword==None:
            keyword=''
        results = redis_search_positions(keyword,Position)
        results_per_page = 6  # 每页显示6条结果  
        page = int(request.args.get('page', 1))  # 获取当前页码，默认为1 
        page_results, total_pages = get_total_pages(results,results_per_page,page)
        
        return render_template('index.html',results=page_results,keyword=keyword,total_pages=total_pages,page=page)



@bp.route('/logout',methods=['GET','POST'])
def logout():
    session.clear()
    return redirect('/')