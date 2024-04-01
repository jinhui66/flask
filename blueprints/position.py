from flask import Blueprint
from flask import Flask,request,render_template,session,redirect,url_for
from flask_sqlalchemy import SQLAlchemy
from redis import Redis
from exts import db,mail,xtredis
from models.table import User, Resume, Position, Comment
import json

bp = Blueprint('position',__name__,url_prefix='/')
 
@bp.route('/position_detail_action', methods=['GET','POST'])
def action():
    if request.method == 'GET':
        result_id = request.args.get('position_id')
        session['position_id'] = result_id
        return redirect(url_for('position.position_detail'))
    else:
        pass

@bp.route('/position_detail', methods=['GET','POST'])
def position_detail():
    if request.method == 'GET':
        # result_id = request.args.get('position_id')
        result_id = session['position_id']
        position = Position.query.filter_by(id=result_id).first()
        comments = Comment.query.filter_by(position_id=result_id).order_by(Comment.time.desc())
        return render_template('menu/position_detail.html',position=position,comments=comments)
    if request.method == 'POST':
        pass

@bp.route('/position_comment',methods=['GET','POST'])
def position_comment():
    if request.method == 'GET':
        pass
    else:
        user_id = session.get('user_id')
        page = request.form.get('page')
        position_id = request.form.get('position_id')
        position = Position.query.filter_by(id=position_id).first()
        content = request.form.get('content')
        comment = Comment(content=content,position_id=position.id,user_id=user_id)
        db.session.add(comment)
        db.session.commit()
        return redirect(url_for('position.position_detail'))