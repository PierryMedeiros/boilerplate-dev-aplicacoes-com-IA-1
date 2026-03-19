from flask import Flask, jsonify, request
from flask_cors import CORS
import controllers
from database import get_db

# SMELL: Secret key hardcoded
app = Flask(__name__)
app.config["SECRET_KEY"] = "minha-chave-super-secreta-123"
app.config["DEBUG"] = True  # SMELL: Debug em produção
CORS(app)  # SMELL: CORS liberado para tudo

# SMELL: Rotas definidas manualmente sem usar Blueprint ou qualquer organização
# SMELL: Mistura de responsabilidades - arquivo de rotas fazendo setup de app

# Produtos
app.add_url_rule("/produtos", "listar_produtos", controllers.listar_produtos, methods=["GET"])
app.add_url_rule("/produtos/busca", "buscar_produtos", controllers.buscar_produtos, methods=["GET"])
app.add_url_rule("/produtos/<int:id>", "buscar_produto", controllers.buscar_produto, methods=["GET"])
app.add_url_rule("/produtos", "criar_produto", controllers.criar_produto, methods=["POST"])
app.add_url_rule("/produtos/<int:id>", "atualizar_produto", controllers.atualizar_produto, methods=["PUT"])
app.add_url_rule("/produtos/<int:id>", "deletar_produto", controllers.deletar_produto, methods=["DELETE"])

# Usuarios
app.add_url_rule("/usuarios", "listar_usuarios", controllers.listar_usuarios, methods=["GET"])
app.add_url_rule("/usuarios/<int:id>", "buscar_usuario", controllers.buscar_usuario, methods=["GET"])
app.add_url_rule("/usuarios", "criar_usuario", controllers.criar_usuario, methods=["POST"])
app.add_url_rule("/login", "login", controllers.login, methods=["POST"])

# Pedidos
app.add_url_rule("/pedidos", "criar_pedido", controllers.criar_pedido, methods=["POST"])
app.add_url_rule("/pedidos", "listar_todos_pedidos", controllers.listar_todos_pedidos, methods=["GET"])
app.add_url_rule("/pedidos/usuario/<int:usuario_id>", "listar_pedidos_usuario", controllers.listar_pedidos_usuario, methods=["GET"])
app.add_url_rule("/pedidos/<int:pedido_id>/status", "atualizar_status_pedido", controllers.atualizar_status_pedido, methods=["PUT"])

# Relatorios
app.add_url_rule("/relatorios/vendas", "relatorio_vendas", controllers.relatorio_vendas, methods=["GET"])

# Health
app.add_url_rule("/health", "health_check", controllers.health_check, methods=["GET"])


# SMELL: Rota duplicada/alternativa desnecessária
@app.route("/")
def index():
    return jsonify({
        "mensagem": "Bem-vindo à API da Loja",
        "versao": "1.0.0",
        "endpoints": {
            "produtos": "/produtos",
            "usuarios": "/usuarios",
            "pedidos": "/pedidos",
            "login": "/login",
            "relatorios": "/relatorios/vendas",
            "health": "/health"
        }
    })


# SMELL: Rota de "admin" sem nenhuma autenticação
@app.route("/admin/reset-db", methods=["POST"])
def reset_database():
    """PERIGOSO: Reseta todo o banco de dados"""
    db = get_db()
    cursor = db.cursor()
    cursor.execute("DELETE FROM itens_pedido")
    cursor.execute("DELETE FROM pedidos")
    cursor.execute("DELETE FROM produtos")
    cursor.execute("DELETE FROM usuarios")
    db.commit()
    print("!!! BANCO DE DADOS RESETADO !!!")
    return jsonify({"mensagem": "Banco de dados resetado", "sucesso": True}), 200


# SMELL: Rota que faz query SQL direta via parâmetro (extremamente perigoso)
@app.route("/admin/query", methods=["POST"])
def executar_query():
    """EXTREMAMENTE PERIGOSO: Executa SQL arbitrário"""
    dados = request.get_json()
    query = dados.get("sql", "")
    if not query:
        return jsonify({"erro": "Query não informada"}), 400

    db = get_db()
    cursor = db.cursor()
    try:
        cursor.execute(query)
        if query.strip().upper().startswith("SELECT"):
            rows = cursor.fetchall()
            result = [dict(row) for row in rows]
            return jsonify({"dados": result, "sucesso": True}), 200
        else:
            db.commit()
            return jsonify({"mensagem": "Query executada", "sucesso": True}), 200
    except Exception as e:
        return jsonify({"erro": str(e)}), 500


if __name__ == "__main__":
    # SMELL: Força inicialização do banco no import
    get_db()
    print("=" * 50)
    print("SERVIDOR INICIADO")
    print("Rodando em http://localhost:5000")
    print("=" * 50)
    # SMELL: host 0.0.0.0 expõe para toda a rede, debug=True em produção
    app.run(host="0.0.0.0", port=5000, debug=True)
