from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysql://joaovitotcaldeir:toledo22@joaovitorcaldeira.mysql.pythonanywhere-services.com:3306/joaovitorcaldeir$mydb'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ecommerce.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

class Usuario(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    senha = db.Column(db.String(100), nullable=False)

class Anuncio(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(100), nullable=False)
    descricao = db.Column(db.Text, nullable=False)
    preco = db.Column(db.Float, nullable=False)
    categoria_id = db.Column(db.Integer, db.ForeignKey('categoria.id'), nullable=False)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)

class Categoria(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)

@login_manager.user_loader
def load_user(user_id):
    return Usuario.query.get(int(user_id))

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']
        senha = request.form['senha']
        usuario = Usuario(nome=nome, email=email, senha=senha)
        db.session.add(usuario)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('cadastro.html')

@app.route('/anuncios', methods=['GET', 'POST'])
@login_required
def anuncios():
    if request.method == 'POST':
        titulo = request.form['titulo']
        descricao = request.form['descricao']
        preco = request.form['preco']
        categoria_id = request.form['categoria']
        usuario_id = current_user.id
        anuncio = Anuncio(titulo=titulo, descricao=descricao, preco=preco, usuario_id=usuario_id, categoria_id=categoria_id)
        db.session.add(anuncio)
        db.session.commit()
        return redirect(url_for('anuncios'))
    categorias = Categoria.query.all()
    return render_template('anuncios.html', categorias=categorias)

@app.route('/perfil')
@login_required
def perfil():
    return render_template('perfil.html')

@app.route('/relatorios')
@login_required
def relatorios():
    return render_template('relatorios.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        senha = request.form['senha']
        usuario = Usuario.query.filter_by(email=email, senha=senha).first()
        if usuario:
            login_user(usuario)
            return redirect(url_for('home'))
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
