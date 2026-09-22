from flask import Blueprint, request, session, jsonify
from app import get_db

api_adicionar = Blueprint('api_adicionar', __name__)


@api_adicionar.route('/api/adicionar', methods=['POST'])
def adicionar_produto():

    if 'logado' not in session:
        return jsonify({
            "erro": "Usuário não está logado"
        }), 401

    if session.get('validade') == 0:
        return jsonify({
            "erro": "Usuário banido"
        }), 403

    if session.get('permisao') != 0:
        return jsonify({
            "erro": "Sem permissão para adicionar produtos"
        }), 403

    dados = request.get_json(silent=True)

    if not dados:
        return jsonify({
            "erro": "JSON inválido ou ausente"
        }), 400

    Nome = dados.get('Nome')
    Quantidade = dados.get('Quantidade')
    Preco = dados.get('Preco')
    Categoria = dados.get('Categoria')
    Descricao = dados.get('Descricao')
    Imagem = dados.get('Imagem')

    if not Nome or Quantidade is None or Preco is None:
        return jsonify({
            "erro": "Nome, Quantidade e Preco são obrigatórios"
        }), 400

    db = get_db()
    cursor = db.cursor()

    try:
        cursor.execute("""
            INSERT INTO estoque
            (Nome, Quantidade, Preco, Categoria, Descricao, Imagem)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (
            Nome,
            Quantidade,
            Preco,
            Categoria,
            Descricao,
            Imagem
        ))

        db.commit()

    except Exception as e:
        db.rollback()

        return jsonify({
            "erro": "Erro ao adicionar produto"
        }), 500

    finally:
        cursor.close()

    return jsonify({
        "mensagem": "Produto adicionado com sucesso",
        "Nome": Nome,
        "Quantidade": Quantidade,
        "Preco": Preco,
        "Categoria": Categoria,
        "Descricao": Descricao,
        "Imagem": Imagem
    }), 201
