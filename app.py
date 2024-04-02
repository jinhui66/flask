from flask import Flask,redirect,session,g,send_from_directory  
import config
from exts import db,mail
from flask_migrate import Migrate
from blueprints.user import bp as user_bp
from blueprints.menu import bp as menu_bp
from blueprints.position import bp as position_bp
from blueprints.email import bp as email_bp
from blueprints.admin import bp as admin_bp
from blueprints.load import bp as load_bp
from models.table import User, Admin, Position
import os
# import torch

# 启动
app = Flask(__name__)
app.template_folder = 'templates'

# 配置
app.config.from_object(config)
  
# 默认的静态文件夹仍然是 'static'  
app.static_folder = 'static'  # 可以省略  
  
# 定义第二个静态文件夹的路径  
SECOND_STATIC_FOLDER = 'data'  
  
# 为第二个静态文件夹定义路由  
@app.route('/data/<path:filename>')  
def second_static(filename):  
    return send_from_directory(SECOND_STATIC_FOLDER, filename)  
  
# 确保上传文件夹存在  
if not os.path.exists('data/resumes'):  
    os.makedirs('data/resumes')  
if not os.path.exists('data/pictures'):  
    os.makedirs('data/pictures')  
if not os.path.exists('data/send_resumes'):
    os.mkdir('data/send_resumes')

db.init_app(app)
mail.init_app(app)

migrate = Migrate(app,db)

# 注册蓝图
app.register_blueprint(user_bp)
app.register_blueprint(menu_bp)
app.register_blueprint(position_bp)
app.register_blueprint(email_bp)
app.register_blueprint(admin_bp)
app.register_blueprint(load_bp)

#建表
with app.app_context():
    db.create_all()

@app.before_request
def my_before_request():
    user_id = session.get('user_id')
    type = session.get('type')
    if user_id and type == 'user':
        user = User.query.filter_by(id=user_id).first()
        setattr(g,'user',user)
        setattr(g,'type','user')
    elif user_id and type == 'admin':
        admin = Admin.query.filter_by(id=user_id).first()
        setattr(g,'user',admin)
        setattr(g,'type','admin')
    else:
        setattr(g,'user',None)
        setattr(g,'type',None)
        
    position_id = session.get('position_id')
    if position_id:
        position = Position.query.filter_by(id=position_id).first()
        setattr(g,'position',position)
    else:
        setattr(g,'position',None)
    
@app.context_processor
def my_context_porcessor():
    return {'user':g.user,'type':g.type}

if __name__ == '__main__':
    app.run(debug=True,host='127.0.0.1')
