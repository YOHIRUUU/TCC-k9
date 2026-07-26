#---------IMPORTS DO BALACOBACO--------
from flask import Flask, render_template, g
import mysql.connector 
from flask import request
from flask import redirect
import bcrypt

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
def ganesha():
    if request.method == "POST":
        mail = request.form.get("mail")
        user = request.form.get("user")
        senha = request.form.get("senha")
        if user and mail and senha:
            db = get_db()
            cursor = db.cursor(dictionary=True)
            try:
                buscar_senha = "SELECT senha FROM usuarios WHERE email = %s AND `nome` = %s"
                cursor.execute(buscar_senha, (mail, user))
                usuario = cursor.fetchone()
                if usuario:
                    hash_banco = usuario["senha"]
                    if isinstance(hash_banco, bytes):
                        hash_str = hash_banco.decode("utf-8")
                    else:
                        hash_str = hash_banco
                        hash_banco = hash_banco.encode("utf-8")
                    partes = hash_str.split("$")
                    if len(partes) >= 3 and partes[2] == "12":
                        if bcrypt.checkpw(senha.encode("utf-8"), hash_banco):
                            return redirect("/ABRAXAS", code=302)
                    else:
                        print("O hash informado não possui o fator de custo 12.")
            finally:
                cursor.close()
    return render_template("Ganesha.html")

@app.route("/ABRAXAS")
def ABRAXAS():
    db = get_db()
    cursor = db.cursor(dictionary=True)

    cursor.execute("SELECT * FROM estoque")
    registros = cursor.fetchall()

    cursor.close()

    return render_template("ABRAXAS.html", registros=registros)

@app.route("/Tirthankaras", methods=["GET", "POST"])
def Tirthankaras():
    if request.method == "POST":
        email = request.form.get('mail')
        user = request.form.get('user')
        senha = request.form.get('senha')
        opcao = request.form.get('opcao')
        permissao = 1 if opcao else 0
        if email and user and senha:
            salt = bcrypt.gensalt(rounds=12)
            senha_hash = bcrypt.hashpw(senha.encode('utf-8'), salt)
            senha_hash_str = senha_hash.decode('utf-8')
            db = get_db()
            cursor = db.cursor()
            try:
                sql = """
                INSERT INTO usuarios (email, nome, senha, permisao)
                VALUES (%s, %s, %s, %s)
                """
                cursor.execute(sql, (email, user, senha_hash_str, permissao))
                db.commit()
                return redirect("/ABRAXAS", code=302)
            except Exception as e:
                db.rollback()
                print(f"Erro ao inserir no banco de dados: {e}")
            finally:
                cursor.close()
    return render_template("Tirthankaras.html")

@app.route("/historico")
def historico():
    db = get_db()
    cursor = db.cursor(dictionary=True)

    cursor.execute("SELECT * FROM estoque")
    registros = cursor.fetchall()

    cursor.close()

    return render_template("historico.html", registros=registros)

@app.route("/Bodhisattvas", methods=["GET", "POST"])
def Bodhisattvas():
    if request.method == "POST":
        nome = request.form.get("Nome")
        quantidade = request.form.get("Quantidade")
        preco = request.form.get("Preco")
        categoria = request.form.get("Categoria")
        descricao = request.form.get("Descricao")
        imagem = request.form.get("Imagem")
    

        db = get_db()
        cursor = db.cursor()

        sql = """
        INSERT INTO estoque (nome, quantidade, preco, categoria, descricao, imagem)
        VALUES (%s, %s, %s, %s, %s, %s)
        """

        cursor.execute(sql, (nome, quantidade, preco, categoria, descricao, imagem))
        db.commit()
        cursor.close()

    return render_template("Bodhisattvas.html")

@app.route("/anubis", methods=["GET", "POST"])
def anubis():
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM estoque")
    registros = cursor.fetchall()
    cursor.close()
    if request.method == "POST":
        opcao = request.form.get('opcao')
        if opcao == 'add':
            quant = request.form.get('Quantidade')
            item = request.form.get('item_selecionado')
            id_limpo = int(item) if item and item.isdigit() else None
            if id_limpo and quant:
                db = get_db()
                cursor = db.cursor(dictionary=True)
                query_busca_quant = "SELECT quantidade FROM estoque WHERE id = %s"
                cursor.execute(query_busca_quant, (id_limpo,))
                resultado_quant = cursor.fetchone()
                if resultado_quant:
                    quant_atual = resultado_quant['quantidade']
                    quant3 = quant_atual + int(quant)
                    query_update = "UPDATE estoque SET quantidade = %s WHERE id = %s"
                    cursor.execute(query_update, (quant3, id_limpo))
            db.commit()
            cursor.close()
        else:
            quant = request.form.get('Quantidade')
            item = request.form.get('item_selecionado')
            id_limpo = int(item) if item and item.isdigit() else None
            if id_limpo and quant:
                db = get_db()
                cursor = db.cursor(dictionary=True)
                query_busca_quant = "SELECT quantidade FROM estoque WHERE id = %s"
                cursor.execute(query_busca_quant, (id_limpo,))
                resultado_quant = cursor.fetchone()
                if resultado_quant:
                    quant_atual = resultado_quant['quantidade']
                    quant3 = quant_atual - int(quant)
                    query_update = "UPDATE estoque SET quantidade = %s WHERE id = %s"
                    cursor.execute(query_update, (quant3, id_limpo))
        db.commit()
        cursor.close()
    return render_template("anubis.html", registros=registros)
    
@app.route("/back")
def back():
    return render_template("back.html")
#------------FIM DAS ROTAS BACANAS--------------

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=3000)
