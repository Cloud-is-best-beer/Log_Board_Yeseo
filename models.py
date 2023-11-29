import pymysql

class DB:
    def __init__(self):
        self.connection = None
        
    def connect(self):
        self.connection = pymysql.connect(
            host='127.0.0.1',
            user='root',
            password='',# 본인 비밀번호 대입
            database='log_board',
            charset='utf8'
        )
    def disconnect(self):
        if self.connection:
            self.connection.close()
    
    def execute_query(self, query, data=None):
        try:
            cursor = self.connection.cursor()
            cursor.execute(query, data)
            self.connection.commit()
            return cursor.fetchall()
        
        except pymysql.Error as e:
            print(f"Error: {e}")
            return None

def get_posts():
    db = DB()
    db.connect()
    query = "SELECT * FROM post"
    posts = db.execute_query(query)
    column_names = ["id", "title", "contents", "user", "date"]
    dict_posts = [dict(zip(column_names, post)) for post in posts]
    db.disconnect()
    return dict_posts
    
    