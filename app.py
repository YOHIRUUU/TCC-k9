#---------IMPORTS DO BALACOBACO?--------
from flask import Flask, render_template, g, request, redirect, session
import mysql.connector 
import bcrypt

#---------FIM DOS IMPORTS---------

app = Flask(__name__)
app.secret_key = "7ae8e5ccbd9e2e5310a579f7ef1c9fc4911ffda504244469c197eb45ca8785ef5afd5e821b189d430877d7f0c2011047"

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
#--------------antigo ganesha---------------
@app.route("/", methods=["GET", "POST"])
def logar():
    if request.method == "POST":
        mail = request.form.get("mail")
        user = request.form.get("user")
        senha = request.form.get("senha")
        if user and mail and senha:
            db = get_db()
            cursor = db.cursor(dictionary=True)
            try:
                buscar_senha = "SELECT senha, permisao, validade FROM usuarios WHERE email = %s AND `nome` = %s"
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
                            session['logado'] = True
                            session['email'] = mail
                            session['nome'] = user
                            session['permisao'] = usuario['permisao']
                            session['validade'] = usuario['validade']
                            return redirect("/ABRAXAS", code=302)
                    else:
                        print("O hash informado não possui o fator de custo 12.")
            finally:
                cursor.close()
    return render_template("logar.html")

#--------------o mesmo ABRAXAS---------------
@app.route("/ABRAXAS", methods=["GET", "POST"])
def ABRAXAS():
    if 'logado' not in session:
        return redirect("/")
    if session.get('validade') == 0:
        return redirect("/banido")
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM estoque")
    registros = cursor.fetchall()
    cursor.close()
    return render_template("ABRAXAS.html", registros=registros)

#--------------o antigo Tithankaras---------------
@app.route("/cadastrar", methods=["GET", "POST"])
def cadastrar():
    if 'logado' not in session:
        return redirect("/")
    if session.get('permisao') == 0:
        return redirect("/ABRAXAS")
    if session.get('validade') == 0:
        return redirect("/banido")
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
    return render_template("cadastrar.html")

#--------------O mesmo historico---------------
@app.route("/historico")
def historico():
    if 'logado' not in session:
        return redirect("/")
    if session.get('validade') == 0:
        return redirect("/banido")
    db = get_db()
    cursor = db.cursor(dictionary=True)
    query = "SELECT * FROM historico_estoque ORDER BY data_hora DESC LIMIT 15"
    cursor.execute(query)
    registros = cursor.fetchall()
    cursor.close()
    return render_template("historico.html", registros=registros)

#---------antigo Bodhisattvas------------
@app.route("/adicionar", methods=["GET", "POST"])
def adicionar():
    if 'logado' not in session:
        return redirect("/")
    if session.get('permisao') == 0:
        return redirect("/ABRAXAS")
    if session.get('validade') == 0:
        return redirect("/banido")
    if request.method == "POST":
        email = session.get('email')
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
        query_historico = """
        UPDATE historico_estoque
        SET email = %s
        WHERE (email IS NULL OR email = '')
        ORDER BY id_log DESC
        LIMIT 1;
        """
        cursor.execute(query_historico, (email,))
        db.commit()
        cursor.close()
    return render_template("adicionar.html")

#--------------o antigo anubis---------------
@app.route("/movimentação", methods=["GET", "POST"])
def movimento():
    if 'logado' not in session:
        return redirect("/")
    if session.get('validade') == 0:
        return redirect("/banido")
    db = get_db()
    cursor = db.cursor(dictionary=True)
    if request.method == "POST":
        opcao = request.form.get('opcao')
        quant = request.form.get('Quantidade')
        item = request.form.get('item_selecionado')
        email = session.get('email')
        id_limpo = int(item) if item and item.isdigit() else None
        quant_limpa = int(quant) if quant and quant.isdigit() else 0
        if id_limpo and quant_limpa > 0:
            cursor.execute("SELECT quantidade FROM estoque WHERE id = %s", (id_limpo,))
            resultado_quant = cursor.fetchone()
            if resultado_quant:
                quant_atual = resultado_quant['quantidade']
                if opcao == 'add':
                    nova_quant = quant_atual + quant_limpa
                else:
                    nova_quant = quant_atual - quant_limpa
                cursor.execute("UPDATE estoque SET quantidade = %s WHERE id = %s", (nova_quant, id_limpo))
                query_historico = """
                UPDATE historico_estoque
                SET email = %s
                WHERE (email IS NULL OR email = '')
                ORDER BY id_log DESC
                LIMIT 1;
                """
                cursor.execute(query_historico, (email,))
                db.commit()
    cursor.execute("SELECT * FROM estoque")
    registros = cursor.fetchall()
    cursor.close()
    return render_template("movimento.html", registros=registros)

#--------------o antigo anu---------------
@app.route("/remover", methods=["GET", "POST"])
def remover():
    if 'logado' not in session:
        return redirect("/")
    if session.get('permisao') == 0:
        return redirect("/ABRAXAS")
    if session.get('validade') == 0:
        return redirect("/banido")
    email = session.get('email')
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM estoque")
    registros = cursor.fetchall()
    cursor.close()
    if request.method == "POST":
        item = request.form.get('item_selecionado')
        if item:
            db = get_db()
            cursor = db.cursor(dictionary=True)
            sql = "DELETE FROM estoque WHERE id = %s"
            cursor.execute(sql, (item,))
            query_historico = """
            UPDATE historico_estoque
            SET email = %s
            WHERE (email IS NULL OR email = '')
            ORDER BY id_log DESC
            LIMIT 1;
            """
            cursor.execute(query_historico, (email,))
            db.commit()
            cursor.close()
    return render_template("remover.html", registros=registros)

@app.route("/usuarios")
def users():
    if 'logado' not in session:
        return redirect("/")
    if session.get('permisao') == 0:
        return redirect("/ABRAXAS")
    if session.get('validade') == 0:
        return redirect("/banido")
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM usuarios")
    registros = cursor.fetchall()
    cursor.close()
    return render_template("users.html", registros=registros)

@app.route("/perfil")
def perfil():
    if 'logado' not in session:
        return redirect("/")
    if session.get('validade') == 0:
        return redirect("/banido")
    email = session.get('email')
    db = get_db()
    cursor = db.cursor(dictionary=True)
    siquel = "SELECT * FROM historico_estoque WHERE email = %s"
    cursor.execute(siquel, (email,))
    registros = cursor.fetchall()
    sequel = "SELECT * FROM usuarios WHERE email = %s"
    cursor.execute(sequel, (email,))
    registro = cursor.fetchall()
    cursor.close()
    return render_template("perfil.html", registros=registros, registro=registro)

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

@app.route("/delete")
def delete():
    email = session.get('email')
    db = get_db()
    cursor = db.cursor(dictionary=True)
    siquel = "DELETE FROM usuarios WHERE email = %s"
    cursor.execute(siquel, (email,))
    db.commit()
    cursor.close()
    session.clear()
    return redirect("/")

@app.route("/banir", methods=["GET", "POST"])
def banir():
    if 'logado' not in session:
        return redirect("/")
    if session.get('permisao') == 0:
        return redirect("/perfil")
    if session.get('validade') == 0:
        return redirect("/banido")
    emeil = session.get('email')
    db = get_db()
    cursor = db.cursor(dictionary=True)
    siquel = "SELECT * FROM usuarios WHERE email <> %s AND validade = 1"
    cursor.execute(siquel, (emeil,))
    registros = cursor.fetchall()
    if request.method == "POST":
        email = request.form.get('email_selecionado')
        if email:
            db = get_db()
            cursor = db.cursor(dictionary=True)
            sql = "UPDATE usuarios SET validade = 0 WHERE email = %s"
            cursor.execute(sql, (email,))
            db.commit()
            cursor.close()
    return render_template("banir.html", registros = registros)

@app.route("/desbanir", methods=["GET", "POST"])
def desbanir():
    if 'logado' not in session:
        return redirect("/")
    if session.get('permisao') == 0:
        return redirect("/perfil")
    if session.get('validade') == 0:
        return redirect("/banido")
    db = get_db()
    cursor = db.cursor(dictionary=True)
    siquel = "SELECT * FROM usuarios WHERE validade = 0"
    cursor.execute(siquel,)
    registros = cursor.fetchall()
    if request.method == "POST":
        email = request.form.get('email_selecionado')
        if email:
            db = get_db()
            cursor = db.cursor(dictionary=True)
            sql = "UPDATE usuarios SET validade = 1 WHERE email = %s"
            cursor.execute(sql, (email,))
            db.commit()
            cursor.close()
    return render_template("desbanir.html", registros = registros)

@app.route("/banido")
def banido():
    return render_template("banido.html")

@app.route("/back")
def back():
    return render_template("back.html")
#------------FIM DAS ROTAS BACANAS--------------

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=3000)
