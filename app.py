from flask import Flask, render_template, g
import mysql.connector 
from mysql.connector import Error
import os
import logging

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

#----------SQL------------------
DB_HOST = os.getenv('DB_HOST','localhost')
DB_USER = os.getenv('DB_USER','root')
DB_PASSWORD = os.getenv('DB_PASSWORD','')
DB_DATABASE = os.getenv('DB_DATABASE','almoxarifado')

def get_db():
    """Abre uma conexão com o banco de dados se já não houver uma ativa na requisição."""
    if 'db' not in g:
        g.db = mysql.connector.connect(
            host=localhost,
            user=root,
            password=,
            database=almoxarifado
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
def index():
    return render_template("Index.html")


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=3000)
