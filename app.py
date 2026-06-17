from flask import Flask
import mysql.connector 
import os

app = Flask(__name__)

#----------SQL------------------
DB_HOST = 'localhost'
DB_USER = 'seu_usuario'
DB_PASSWORD = 'sua_senha'
DB_DATABASE = 'seu_banco'

def get_db():
    """Abre uma conexão com o banco de dados se já não houver uma ativa na requisição."""
    if 'db' not in g:
        g.db = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_DATABASE
        )
    return g.db

@app.teardown_appcontext
def close_db(e):
    """Fecha a conexão com o banco de dados ao final da requisição."""
    db = g.pop('db', None)
    if db is not None:
        db.close()

#--------------FIM DO SQL--------------------

@app.route("/")
def home():
    return "WAAAAAAH"


if __name__ == "__main__":
    app.run(debug=True)
