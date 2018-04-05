# -*- coding: utf-8 -*-

from flask import Flask, render_template, request, redirect, url_for
import config
from models import User, Question, Comment
from exts import db
from flask import session
from decorators import login_required

app = Flask(__name__)
app.config.from_object(config)
db.init_app(app)


@app.route('/')
def index():
    context = {
        'questions': Question.query.order_by('-create_time').all()
    }
    return render_template('index.html', **context)


@app.route('/login/', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        telephone = request.form.get('telephone')
        pasword = request.form.get('password')
        user = User.query.filter(User.telephone == telephone, User.password == pasword).first()
        if user:
            session['user_id'] = user.id
            session.permanent = True
            return redirect(url_for('index'))
        else:
            return u'手机号码或者密码错误，请确认后再登录'


@app.route('/regist/', methods=['GET', 'POST'])
def regist():
    if request.method == 'GET':
        return render_template('register.html')
    else:
        phone_num = request.form.get('phone_num')
        username = request.form.get('username')
        password = request.form.get('password')
        confirm = request.form.get('confirm')

        user = User.query.filter(User.telephone == phone_num).first()
        if user:
            return u'该手机号码已经被注册，请更换手机号码!'
        else:
            if password != confirm:
                return u'两次密码不相等，请核对后再填写'
            else:
                user = User(telephone=phone_num, username=username, password=password)
                db.session.add(user)
                db.session.commit()
                return redirect(url_for('login'))


@app.route('/question/', methods=['GET', 'POST'])
@login_required
def question():
    if request.method == 'GET':
        return render_template('question.html')
    else:
        title = request.form.get('title')
        content = request.form.get('content')
        question = Question(title=title, content=content)
        user_id = session.get('user_id')
        user = User.query.filter(User.id == user_id).first()
        question.author = user
        db.session.add(question)
        db.session.commit()
        return redirect(url_for('index'))


@app.route('/detail/<question_id>/')
def detail(question_id):
    question_model = Question.query.filter(Question.id == question_id).first()
    return render_template('detail.html', question=question_model)


@app.route('/comment/', methods=['POST'])
@login_required
def comment():
    content = request.form.get('comment')
    question_id = request.form.get('question_id')
    comment = Comment(content=content)
    user_id = session.get('user_id')
    user = User.query.filter(User.id == user_id).first()
    comment.author = user
    question = Question.query.filter(Question.id == question_id).first()
    comment.question = question
    db.session.add(comment)
    db.session.commit()
    return redirect(url_for('detail', question_id=question_id))


@app.context_processor
def my_context_processor():
    user_id = session.get('user_id')
    if user_id:
        user = User.query.filter(User.id == user_id).first()
        if user:
            return {'user': user}
    return {}


if __name__ == '__main__':
    app.run()
