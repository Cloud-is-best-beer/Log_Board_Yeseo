# runs.py

from flask import Flask, request, redirect, render_template, url_for, session, flash
from models import DB, get_posts
from datetime import datetime
import secrets

app = Flask(__name__) 
app.secret_key = secrets.token_hex(16)
db = DB()

@app.route('/')
def home():
    posts = get_posts()
    reversed_posts = posts[::-1]
    return render_template('home.html', posts=reversed_posts)

@app.route('/login', methods =['GET', 'POST'])
def login(): # 로그인
    if request.method =='POST':
        db.connect()
        user_id = request.form['id']
        user_pw = request.form['password']
        query = f"SELECT * FROM users WHERE id='{user_id}' AND password='{user_pw}'"
        result = db.execute_query(query)
        print('result = ',result)
        
        if result: # 로그인 성공
            print('login success',user_id)
            session['user_id'] = user_id # 아이디 세션 저장
            db.disconnect()
            return redirect(url_for('home')) #HOME 페이지로 이동
        else: # 로그인 실패
            print('login fail')
            flash('아이디 또는 비밀번호가 올바르지 않습니다.')
            db.disconnect()
            return render_template('login.html')
        
    else:
        return render_template('login.html')
    
@app.route('/signup', methods =['GET', 'POST'])
def signup(): # 회원가입
    if request.method =='POST':
        db.connect()
        new_id = request.form['id']
        new_pw = request.form['password']
        new_name = request.form['name']
        query = f"SELECT * FROM users WHERE id='{new_id}'"
        result = db.execute_query(query)
        
        if result:
            flash('사용할 수 없는 아이디입니다. 다른 아이디를 입력해 주세요.')
            return render_template('signup.html')
        else:
            query = f"INSERT INTO users (id, password, name) values ('{new_id}','{new_pw}','{new_name}')"
            db.execute_query(query)
            print('signup success',new_id)
            db.disconnect()
            return redirect(url_for('home')) #HOME 페이지로 이동 
            
    else:
        return render_template('signup.html')

@app.route('/logout')
def logout(): # 로그아웃
    session.pop('user_id', None)
    return redirect(url_for('home'))

@app.route('/writePost', methods =['GET', 'POST'])
def write_post(): # 게시글 작성
    if request.method =='POST':  
        title = request.form['title']
        contents = request.form['contents']
        
        if title.strip() == "" or contents.strip() =="": # 게시글 제목, 내용 빈칸일 때
            flash('제목과 내용을 모두 입력해주세요.')
            return render_template('write_post.html', title=title, contents=contents)
        else:
            print(title, contents)
            user = session['user_id']
            today=datetime.today()
            date = today.strftime('%Y-%m-%d')
            
            db.connect()
            query = f"INSERT INTO post (post_title, post_contents, post_user, post_date) values ('{title}','{contents}','{user}','{date}')"
            result = db.execute_query(query)
            print('post submit success',title)
            db.disconnect()
            return redirect(url_for('home'))
        
    else:
        return render_template('write_post.html')
    
@app.route('/post/<int:id>/')
def view_post(id): # 게시글 확인
    posts = get_posts()
    for post in posts:
        if post['id']==id:
            return render_template('view_post.html', post=post, user_id=session.get('user_id'))
    

@app.route('/post/<int:id>/modify/', methods=['GET', 'POST'])
def modify_post(id): # 게시글 수정
    if request.method == 'POST':
        title = request.form['title']
        contents = request.form['contents']
        
        if title.strip() == "" or contents.strip() == "":
            flash('제목과 내용을 모두 입력해주세요.')
            return render_template('modify_post.html', post={'id': id, 'title': title, 'contents': contents})
        else:
            db.connect()
            query = f"UPDATE post SET post_title='{title}', post_contents='{contents}' WHERE post_id={id}"
            result = db.execute_query(query)
            print('post modify success', title)
            db.disconnect()
            return redirect(url_for('view_post', id=id))
        
    else:
        posts = get_posts()
        for post in posts:
            if id == post['id']:
                p = post
        return render_template('modify_post.html', post=p)
        

@app.route('/post/<int:id>/delete/')
def delete_post(id): # 게시글 삭제
    posts = get_posts()
    for post in posts:
        if id == post['id']:
            db.connect()
            query = f"DELETE FROM post WHERE post_id='{id}'"
            result = db.execute_query(query)
            print('post delete success', id)
            db.disconnect()
            return redirect(url_for('home'))

    

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)