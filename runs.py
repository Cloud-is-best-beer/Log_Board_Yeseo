# runs.py

from flask import Flask, request, redirect, render_template, url_for, session, flash
from models import DB
import secrets

app = Flask(__name__) 
app.secret_key = secrets.token_hex(16)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/login', methods =['GET', 'POST'])
def login(): # 로그인
    db = DB()
    db.connect()
    if request.method =='POST':
        user_id = request.form['id']
        user_pw = request.form['password']
        query = f"SELECT * FROM users WHERE id='{user_id}' AND password='{user_pw}'"
        result = db.execute_query(query)
        
        if result: # 로그인 성공
            print('login success',user_id)
            session['user_id'] = user_id
            return redirect(url_for('home'))
        else: # 로그인 실패
            print('login fail')
            flash('아이디 또는 비밀번호가 올바르지 않습니다.')
            return render_template('login.html')
        
    else:
        return render_template('login.html')
    
# @app.route('/signup')
# def signup(): # 회원가입

@app.route('/logout')
def logout(): # 로그아웃
    session.pop('user_id', None)
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)