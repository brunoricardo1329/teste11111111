import os
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv

# Carrega as variáveis do arquivo .env para o ambiente
load_dotenv()

# Inicializa a aplicação Flask
app = Flask(__name__)

# --- CONFIGURAÇÃO SEGURA DO BANCO DE DADOS ---
# Pega a URL do banco de dados da variável de ambiente
DATABASE_URL = os.environ.get('DATABASE_URL')

app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# --- DEFINIÇÃO DA TABELA 'PESSOA' ---
class Pessoa(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)

    def __repr__(self):
        return f'<Pessoa {self.nome}>'

# Garante que a tabela seja criada no banco de dados
with app.app_context():
    db.create_all()

# --- ROTAS DA APLICAÇÃO ---
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        nova_pessoa = Pessoa(nome=request.form['nome'], email=request.form['email'])
        try:
            db.session.add(nova_pessoa)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            print(f"Erro ao inserir no banco: {e}")
        return redirect(url_for('index'))

    pessoas = Pessoa.query.all()
    return render_template('index.html', pessoas=pessoas)

# --- RODA A APLICAÇÃO ---
if __name__ == '__main__':
    # O host='0.0.0.0' permite acesso de outros dispositivos na sua rede
    app.run(host='0.0.0.0', port=5000, debug=True)