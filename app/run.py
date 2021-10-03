from flask import request, jsonify
from model import Usuario, app, db
from sqlalchemy import *

@app.route("/")
def index():
    try:
        message = {"message": "Olá, mundo!", "status": 200}
    except:
        return "Error"

    return  jsonify(message)


@app.route("/cria_tabelas_teste_db")
def cria_tabelas_teste_db():
    
    engine = create_engine('postgresql://postgres:postgres@db:5432/postgres', echo=True)
    metadata = MetaData()

    """Tabela de usuário"""
    usuario = Table('usuario', metadata,
                    #Column('id', Integer, Sequence('usuario_id_seq'), primary_key=True),
                    Column('id', Integer, primary_key=True),
                    Column('nome', String),
                    Column('email', String),
                    Column('senha', String),
                    )

    metadata.create_all(engine)

    return "Tabela criada com sucesso!!"

@app.route("/usuarios", methods=["GET", "POST"])
def usuarios():
    if request.method=="GET":
        usuarios = Usuario.query.all()
        lista_de_usuarios = []

        for usr in usuarios:
            lista_de_usuarios.append({
                "id": usr.id,
                "nome": usr.nome,
                "email": usr.email,
                "senha":usr.senha
            })
        
        return jsonify(lista_de_usuarios)

@app.route("/insere_usuarios", methods=["GET", "POST"])
def insere_usuarios():
    if request.method=="POST":
        return insert_banco()

def insert_banco():
    
    id = request.get_json()["id"]
    nome = request.get_json()["nome"]
    email = request.get_json()["email"]
    senha = request.get_json()["senha"]

    usuario = Usuario(id, nome, email, senha)

    usuario_adicionado = {
        "id": id,
        "nome": nome,
        "email": email,
        "senha": senha
    }
    
    try:
        db.session.add(usuario)
        db.session.commit()
        message = {"message": "Usuário adicionado com sucesso", "user": usuario_adicionado}
    except:
        return "Error 500"

    return jsonify(message)


if __name__=="__main__":
    app.run(host="0.0.0.0", debug=True)