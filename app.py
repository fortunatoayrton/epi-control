from flask import Flask, request, jsonify
import psycopg2
import os
from datetime import datetime

app = Flask(__name__)

# =========================
# Conexão com o banco (Render + Supabase)
# =========================
def get_conn():
    return psycopg2.connect(
        host=os.environ.get("DB_HOST"),
        database=os.environ.get("DB_NAME"),
        user=os.environ.get("DB_USER"),
        password=os.environ.get("DB_PASSWORD"),
        port=os.environ.get("DB_PORT")
    )

# =========================
# Rota inicial
# =========================
@app.route('/')
def home():
    return "Sistema EPI ONLINE 🚀"

# =========================
# Listar EPI
# =========================
@app.route('/epi', methods=['GET'])
def listar_epi():
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute("SELECT id, nome, quantidade_total FROM epi;")
    dados = cursor.fetchall()
    conn.close()

    return jsonify([
        {"id": d[0], "nome": d[1], "quantidade": d[2]}
        for d in dados
    ])

# =========================
# Registrar entrega
# =========================
@app.route('/entrega', methods=['POST'])
def entrega():
    data = request.json

    id_usuario = data['id_usuario']
    id_epi = data['id_epi']
    quantidade = data['quantidade']

    conn = get_conn()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO entrega (id_usuario, id_epi, quantidade, data_entrega)
        VALUES (%s, %s, %s, %s)
    """, (id_usuario, id_epi, quantidade, datetime.now()))

    cursor.execute("""
        UPDATE epi
        SET quantidade_total = quantidade_total - %s
        WHERE id = %s
    """, (quantidade, id_epi))

    conn.commit()
    conn.close()

    return jsonify({"status": "Entrega registrada com sucesso"})

# =========================
# Rodar app
# =========================
if __name__ == "__main__":
    app.run()