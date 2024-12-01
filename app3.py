from flask import Flask, render_template, request, jsonify, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os

app = Flask(__name__)

# Configuração do MySQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root@localhost/database_name'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'secret-key'

db = SQLAlchemy(app)

# Modelo de Denúncia
class Denuncia(db.Model):
    __tablename__ = 'denuncias'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(100), nullable=False)
    categoria = db.Column(db.String(50), nullable=False)
    descricao = db.Column(db.Text, nullable=True)
    localizacao = db.Column(db.String(100), nullable=True)
    imagem = db.Column(db.String(200), nullable=True)
    data_envio = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.Boolean, default=False)  # Status: False = Pendente, True = Concluído

# Rota para exibir todas as denúncias
@app.route('/')
def index():
    denuncias = Denuncia.query.all()
    return render_template('index2.html', denuncias=denuncias)

# API para alterar status da denúncia
@app.route('/atualizar_status/<int:denuncia_id>', methods=['POST'])
def atualizar_status(denuncia_id):
    denuncia = Denuncia.query.get_or_404(denuncia_id)
    denuncia.status = True  # Define como concluído
    db.session.commit()
    return jsonify({"success": True})

# API para buscar as localizações das denúncias
@app.route('/api/localizacoes', methods=['GET'])
def api_localizacoes():
    denuncias = Denuncia.query.all()
    localizacoes = [
        {
            "id": denuncia.id,
            "nome": denuncia.nome,
            "categoria": denuncia.categoria,
            "descricao": denuncia.descricao,
            "localizacao": denuncia.localizacao,
            "status": denuncia.status,
        }
        for denuncia in denuncias if denuncia.localizacao
    ]
    return jsonify(localizacoes)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5003))  
    app.run(host='0.0.0.0', port=port, debug=True)
