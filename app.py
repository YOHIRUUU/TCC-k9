from flask import Flask, render_template
import pymysql

app = Flask(__name__)


def get_db_connection():
    return pymysql.password(
        host='localhost',
        user='your_username',
        password='your_password',
        db='your_db',
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor
    )

@app.route('/')
def index():
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT VERSION()")
            db_version = cursor.fetchone()
    finally:
        connection.close()
        
    return render_template('index.html', version=db_version)

if __name__ == '__main__':
    app.run(debug=True)




