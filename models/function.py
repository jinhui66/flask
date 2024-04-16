
from exts import db,mail,xtredis
import json
from models.forms import RegisterForm,LoginForm,ForgotForm
from datetime import datetime, date
from sqlalchemy import or_
import fitz # pip install PyMuPDF

def get_total_pages(results,results_per_page,page):
    # 计算当前页的结果  
    start_index = (page - 1) * results_per_page  
    end_index = start_index + results_per_page  
    page_results = results[start_index:end_index]  

    total_pages = (len(results) + results_per_page - 1) // results_per_page
    print(total_pages)

    return page_results,total_pages  

def redis_search_positions(keyword,Position):
    cached_data = xtredis.get(keyword)
    if cached_data:
        results_data = json.loads(cached_data)
        # print('从缓存')
    else:
        # print('从数据库')
        if keyword==None:
            results = Position.query.all()
        else:
            results = Position.query.filter(
                or_(Position.position_name.like(f'%{keyword}%'),
                    Position.description.like(f'%{keyword}%'))
                ).all()

        results_data = []
        for result in results:
            if result.public == 1:
                results_data.append({
                "id": result.id,
                "company": result.company,
                "position_name": result.position_name,
                "salary": result.salary,
                "education": result.education,
                "description": result.description,
                "address": result.address,
                "release_time": result.release_time,
                "admin": result.admin.to_dict()
                })
        # print(len(results_data))
        # 序列化用户数据
        results_json = json.dumps(results_data,cls=ComplexEncoder)
        # 使用键将用户数据设置在Redis缓存中
        xtredis.set(keyword, results_json, ex=10)  # 根据需要设置过期时间
        
    return results_data

class ComplexEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(obj, date):
            return obj.strftime('%Y-%m-%d')
        else:
            return json.JSONEncoder.default(self, obj)

def extract_text_from_pdf(pdf_path):
    # 打开PDF文件
    document = fitz.open(pdf_path)
    text = ""
 
    # 遍历每一页
    for page_num in range(len(document)):
        page = document[page_num]
        # 获取文本块
        for block in page.get_text("blocks"):
            text += block[4].strip()  # 获取文本内容
 
    document.close()
    return text