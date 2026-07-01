#---------IMPORTS DO BALACOBACO--------
from flask import Flask, render_template, g
import mysql.connector 
import bcrypt 
from flask import request

#---------FIM DOS IMPORTS---------

app = Flask(__name__)

#----------SQL------------------
DB_HOST = 'localhost'
DB_USER = 'root'
DB_PASSWORD = ''
DB_DATABASE = 'almoxarifado'

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

#--------------ROTAS BACANAS---------------
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/ABRAXAS")
def ABRAXAS():
    db = get_db()
    cursor = db.cursor(dictionary=True)

    cursor.execute("SELECT * FROM estoque")
    registros = cursor.fetchall()

    cursor.close()

    return render_template("ABRAXAS.html", registros=registros)

@app.route("/cadastrar")
def cadastrar():
    return render_template("cadastrar.html")

@app.route("/historico")
def historico():
    db = get_db()
    cursor = db.cursor(dictionary=True)

    cursor.execute("SELECT * FROM estoque")
    registros = cursor.fetchall()

    cursor.close()

    return render_template("historico.html", registros=registros)

@app.route("/adicionar", methods=["GET", "POST"])
def adicionar():
    if request.method == "POST":
        nome = request.form.get("Nome")
        quantidade = request.form.get("Quantidade")
        preco = request.form.get("Preco")
        categoria = request.form.get("Categoria")
        descricao = request.form.get("Descricao")
    

        db = get_db()
        cursor = db.cursor()

        sql = """
        INSERT INTO estoque (nome, quantidade, preco, categoria, descricao)
        VALUES (%s, %s, %s, %s, %s)
        """

        cursor.execute(sql, (nome, quantidade, preco, categoria, descricao))
        db.commit()
        cursor.close()

    return render_template("adicionar.html")

@app.route("/anubis", methods=["GET", "POST"])
def anubis():
    return render_template("anubis.html")

#------------FIM DAS ROTAS BACANAS--------------

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=3000)
