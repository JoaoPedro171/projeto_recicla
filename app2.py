from flask import Flask, request, render_template, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
import os
from datetime import datetime

app = Flask(__name__)

# Configuração para o MySQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root@localhost/database_name'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = 'uploads'
app.secret_key = 'secret-key'

# Configurando o SQLAlchemy
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

# Rota para Página Inicial
@app.route('/')
def index():
    return render_template('index.html')

# Rota para Receber Denúncias
@app.route('/denunciar', methods=['POST'])
def denunciar():
    try:
        # Coletando os dados do formulário
        nome = request.form.get('nome')
        categoria = request.form.get('categoria')
        descricao = request.form.get('descricao', None)
        localizacao = request.form.get('localizacao', None)
        imagem = request.files.get('imagem', None)

        # Validando se os campos obrigatórios foram preenchidos
        if not nome or not categoria:
            flash('Os campos Nome e Categoria são obrigatórios!', 'danger')
            return redirect(url_for('index'))

        # Salvando a imagem, se existir
        filename = None
        if imagem:
            # Garantir que a pasta uploads existe
            if not os.path.exists(app.config['UPLOAD_FOLDER']):
                os.makedirs(app.config['UPLOAD_FOLDER'])
            
            filename = f"{datetime.utcnow().strftime('%Y%m%d%H%M%S')}_{imagem.filename}"
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            imagem.save(filepath)

        # Criando uma nova instância de denúncia
        nova_denuncia = Denuncia(
            nome=nome,
            categoria=categoria,
            descricao=descricao,
            localizacao=localizacao,
            imagem=filename
        )

        # Salvando no banco de dados
        db.session.add(nova_denuncia)
        db.session.commit()

        flash('Denúncia enviada com sucesso!', 'success')
        return redirect(url_for('index'))
    except Exception as e:
        flash(f'Erro ao enviar denúncia: {str(e)}', 'danger')
        return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(port=5000, debug=True)
