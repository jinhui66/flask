from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from redis import Redis

db = SQLAlchemy()
mail = Mail()
# # 命令行 redis-server 启动服务器
xtredis = Redis(host='127.0.0.1',port=6379)