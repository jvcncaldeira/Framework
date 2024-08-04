from flask import Flask, render_template, request, redirect, url_for
from models import db, Usuario, Anuncio, Categoria, Pergunta, Resposta, Compra, Favorito

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ecommerce.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

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
def anuncios():
    if request.method == 'POST':
        titulo = request.form['titulo']
        descricao = request.form['descricao']
        preco = request.form['preco']
        categoria_id = request.form['categoria']
        usuario_id = 1  # Alterar para obter ID do usuário logado
        anuncio = Anuncio(titulo=titulo, descricao=descricao, preco=preco, usuario_id=usuario_id, categoria_id=categoria_id)
        db.session.add(anuncio)
        db.session.commit()
        return redirect(url_for('anuncios'))
    categorias = Categoria.query.all()
    return render_template('anuncios.html', categorias=categorias)

@app.route('/perfil')
def perfil():
    return render_template('perfil.html')

@app.route('/relatorios')
def relatorios():
    return render_template('relatorios.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        senha = request.form['senha']
        usuario = Usuario.query.filter_by(email=email, senha=senha).first()
        if usuario:
            return redirect(url_for('home'))
    return render_template('login.html')

if __name__ == '__main__':
    app.run(debug=True)
