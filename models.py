from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    senha = db.Column(db.String(120), nullable=False)
    anuncios = db.relationship('Anuncio', backref='usuario', lazy=True)
    perguntas = db.relationship('Pergunta', backref='usuario', lazy=True)
    respostas = db.relationship('Resposta', backref='usuario', lazy=True)
    compras = db.relationship('Compra', backref='usuario', lazy=True)
    favoritos = db.relationship('Favorito', backref='usuario', lazy=True)

class Anuncio(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(100), nullable=False)
    descricao = db.Column(db.Text, nullable=False)
    preco = db.Column(db.Float, nullable=False)
    data_criacao = db.Column(db.DateTime, default=db.func.current_timestamp())
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)
    categoria_id = db.Column(db.Integer, db.ForeignKey('categoria.id'), nullable=False)
    perguntas = db.relationship('Pergunta', backref='anuncio', lazy=True)
    compras = db.relationship('Compra', backref='anuncio', lazy=True)
    favoritos = db.relationship('Favorito', backref='anuncio', lazy=True)

class Categoria(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    anuncios = db.relationship('Anuncio', backref='categoria', lazy=True)

class Pergunta(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    texto = db.Column(db.Text, nullable=False)
    data_criacao = db.Column(db.DateTime, default=db.func.current_timestamp())
    anuncio_id = db.Column(db.Integer, db.ForeignKey('anuncio.id'), nullable=False)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)
    respostas = db.relationship('Resposta', backref='pergunta', lazy=True)

class Resposta(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    texto = db.Column(db.Text, nullable=False)
    data_criacao = db.Column(db.DateTime, default=db.func.current_timestamp())
    pergunta_id = db.Column(db.Integer, db.ForeignKey('pergunta.id'), nullable=False)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)

class Compra(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data_compra = db.Column(db.DateTime, default=db.func.current_timestamp())
    anuncio_id = db.Column(db.Integer, db.ForeignKey('anuncio.id'), nullable=False)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)

class Favorito(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    anuncio_id = db.Column(db.Integer, db.ForeignKey('anuncio.id'), nullable=False)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)
