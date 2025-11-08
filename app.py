from flask import Flask, render_template, request, redirect, url_for, flash
from sqlalchemy import text
from database import engine

app = Flask(__name__)
app.secret_key = "chave_secreta"

#---AUTORES ---

#Listar

@app.route("/autores")
def listar_autor():
    with engine.connect() as conn:
        autores = conn.execute(text("SELECT * FROM Autores")).fetchall()
    return render_template("autores/listar_autor.html", autores=autores)

#Cadastrar 

@app.route("/autores/cadastrar_autor", methods=["GET", "POST"])
def cadastrar_autor():
    if request.method == "POST":
        nome = request.form.get("nome")
        nacionalidade = request.form.get("nacionalidade")
        nascimento = request.form.get("nascimento")
        biografia = request.form.get("biografia")

        with engine.begin() as conn:
    
            autor_existente = conn.execute(
                text("SELECT * FROM Autores WHERE Nome_autor = :nome"),
                {"nome": nome}
            ).fetchone()

            if autor_existente:
                flash("Autor já cadastrado!", "error")

            else:
                conn.execute(
                    text("""
                        INSERT INTO Autores 
                            (Nome_autor, Nacionalidade, Data_nascimento, Biografia)
                        VALUES 
                            (:nome, :nacionalidade, :data_nascimento, :biografia)
                    """),
                    {
                        "nome": nome,
                        "nacionalidade": nacionalidade,
                        "data_nascimento": nascimento,
                        "biografia": biografia
                    }
                )
                flash("Autor cadastrado com sucesso!", "success")
        return redirect(url_for("listar_autor"))

    return render_template("autores/cadastrar_autor.html")
       
#Editar

@app.route("/autores/editar_autor/<int:id>", methods=["GET", "POST"])
def editar_autor(id):
    with engine.connect() as conn:
        autor = conn.execute(
            text("SELECT * FROM Autores WHERE ID_autor = :id"), {"id": id}
        ).fetchone()

    if not autor:
        flash("Autor não encontrado!", "error")
        return redirect(url_for("listar_autor"))

    if request.method == "POST":
        nome = request.form.get("nome")
        nacionalidade = request.form.get("nacionalidade")
        nascimento = request.form.get("nascimento")
        biografia = request.form.get("biografia")

        with engine.begin() as conn:
            conn.execute(
                text("""
                    UPDATE Autores
                    SET Nome_autor = :nome,
                        Nacionalidade = :nacionalidade,
                        Data_nascimento = :data_nascimento,
                        Biografia = :biografia
                    WHERE ID_autor = :id
                """),
                {
                    "nome": nome,
                    "nacionalidade": nacionalidade,
                    "data_nascimento": nascimento,
                    "biografia": biografia,
                    "id": id
                }
            )
        flash("Autor atualizado com sucesso!", "success")
        return redirect(url_for("listar_autor"))

    return render_template("autores/editar_autor.html", autor=autor)

#Excluir

@app.route("/autores/excluir_autor/<int:id>")
def excluir_autor(id):
    with engine.begin() as conn:
        conn.execute(
            text("DELETE FROM Autores WHERE ID_autor = :id"),
            {"id": id}
        )
    flash("Autor excluído com sucesso!", "success")
    return redirect(url_for("listar_autor"))


#---EDITORAS ---

# Listar 
@app.route("/editoras")
def listar_editora():
    with engine.connect() as conn:
        editoras = conn.execute(text("SELECT * FROM Editoras")).fetchall()
    return render_template("editoras/listar_editora.html", editoras=editoras)

# Cadastrar
@app.route("/editoras/cadastrar_editora", methods=["GET", "POST"])
def cadastrar_editora():
    if request.method == "POST":
        nome = request.form.get("nome")
        endereco = request.form.get("endereco")

        with engine.begin() as conn:
            editora_existente = conn.execute(
                text("SELECT * FROM Editoras WHERE Nome_editora = :nome"),
                {"nome": nome}
            ).fetchone()

            if editora_existente:
                flash("Editora já cadastrada!", "error")
            else:
                conn.execute(
                    text("""
                        INSERT INTO Editoras (Nome_editora, Endereco_editora)
                        VALUES (:nome, :endereco)
                    """),
                    {"nome": nome, "endereco": endereco}
                )
                flash("Editora cadastrada com sucesso!", "success")
        return redirect(url_for("listar_editora"))

    return render_template("editoras/cadastrar_editora.html")

# Editar 
@app.route("/editoras/editar_editora/<int:id>", methods=["GET", "POST"])
def editar_editora(id):
    with engine.connect() as conn:
        editora = conn.execute(
            text("SELECT * FROM Editoras WHERE ID_editora = :id"),
            {"id": id}
        ).fetchone()

    if not editora:
        flash("Editora não encontrada!", "error")
        return redirect(url_for("listar_editora"))

    if request.method == "POST":
        nome = request.form.get("nome")
        endereco = request.form.get("endereco")

        with engine.begin() as conn:
            conn.execute(
                text("""
                    UPDATE Editoras
                    SET Nome_editora = :nome,
                        Endereco_editora = :endereco
                    WHERE ID_editora = :id
                """),
                {"nome": nome, "endereco": endereco, "id": id}
            )
        flash("Editora atualizada com sucesso!", "success")
        return redirect(url_for("listar_editora"))

    return render_template("editoras/editar_editora.html", editora=editora)

# Excluir 
@app.route("/editoras/excluir_editora/<int:id>")
def excluir_editora(id):
    with engine.begin() as conn:
        conn.execute(
            text("DELETE FROM Editoras WHERE ID_editora = :id"),
            {"id": id}
        )
    flash("Editora excluída com sucesso!", "success")
    return redirect(url_for("listar_editora"))


