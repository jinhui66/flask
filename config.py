
SECRET_KEY = '123456'
# 数据库的配置信息
HOSTNAME = "127.0.0.1"
PORT = 3306
USERNAME = "root"
PASSWORD = "Jh.1385726872488"
DATABASE = "database_learn"
SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{USERNAME}:{PASSWORD}@{HOSTNAME}:{PORT}/{DATABASE}?charset=utf8mb4"
SQLALCHEMY_TRACK_MODIFICATIONS = True
SQLALCHEMY_COMMIT_TEARDOWN = True

# 邮箱配置
MAIL_SERVER = "smtp.qq.com"
MAIL_USER_SSL = True
MAIL_PORT = 587
MAIL_USERNAME = "1303101041@qq.com"
MAIL_PASSWORD = "qsdsugwiquodigjh"
MAIL_DEFAULT_SENDER = "1303101041@qq.com"