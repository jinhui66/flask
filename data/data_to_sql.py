import sys
sys.path.append('../')  # 添加上级目录到系统路径
import csv 
from flask import Flask  
from exts import db  
from models.table import Position
import config
import chardet  

app = Flask(__name__)
app.config.from_object(config)
db.init_app(app)
    
def detect_encoding(filename):
    with open(filename, 'rb') as f:
        result = chardet.detect(f.read())
    return result['encoding']

def read(filename):
    positions = []
    with open(filename, newline='', encoding=detect_encoding(filename),errors='ignore') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            position = Position( 
                company=row['company'],
                position_name=row['title'],
                salary=row['salary'],
                education=row['education'],
                description=row['description'],
                address=row['address']
            )
            positions.append(position)
    return positions

def insert(positions):
    for position in positions:
        db.session.add(position)
    db.session.commit()  
    
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        positions = read('data.csv')
        insert(positions)
        print('成功')