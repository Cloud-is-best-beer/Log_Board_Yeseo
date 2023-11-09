import pymysql

class DB:
    def __init__(self):
        self.connection = None
        
    def connect(self):
        self.connection = pymysql.connect(
            host='127.0.0.1',
            user='root',
            password='dbpw1234',
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
    
    