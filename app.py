from flask import Flask, render_template, request, redirect, url_for, flash
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import text
from database import engine

app = Flask(__name__)
app.secret_key = "chave_secreta"

@app.route('/')
def index():
    return render_template('index.html')

#---Usuários ---

# Cadastro Usuários
@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']
        telefone = request.form['telefone']
        data_inscricao = request.form['data_inscricao']
        senha = request.form['senha']

        hash_senha = generate_password_hash(senha)

        with engine.connect() as conn:
            conn.execute(text("""
                INSERT INTO usuarios (nome_usuario, email, numero_telefone, data_inscricao, multa_atual, senha)
                VALUES (:nome, :email, :telefone, :data, 0.00, :senha)
            """), {"nome": nome, "email": email, "telefone": telefone, "data": data_inscricao, "senha": hash_senha})
            conn.commit()

        flash('Cadastro realizado com sucesso! Faça login.', 'success')
        return redirect(url_for('login'))

    return render_template('usuarios/cadastro.html')

# Login Usuários
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        senha = request.form['senha']

        with engine.connect() as conn:
            usuario = conn.execute(text("SELECT * FROM usuarios WHERE email = :email"), {"email": email}).fetchone()

        if usuario and check_password_hash(usuario.senha, senha):
            session['usuario_id'] = usuario.id_usuario
            session['usuario_nome'] = usuario.nome_usuario
            flash('Login realizado com sucesso!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Email ou senha incorretos.', 'danger')

    return render_template('usuarios/login.html')

# LOGOUT 
@app.route('/logout')
def logout():
    session.clear()
    flash('Logout realizado com sucesso!', 'success')
    return redirect(url_for('index'))

# Listar Gêneros 
@app.route('/generos')
def listar_generos():
    with engine.connect() as conn:
        generos = conn.execute(text("SELECT * FROM generos")).fetchall()
    return render_template('generos/listar_genero.html', dados=generos, tabela='generos')

# Cadastrar Gêneros 
@app.route('/generos/novo', methods=['GET', 'POST'])
def novo_genero():
    if request.method == 'POST':
        nome = request.form['nome']
        with engine.connect() as conn:
            conn.execute(text("INSERT INTO generos (nome_genero) VALUES (:nome)"), {"nome": nome})
            conn.commit()
        flash('Gênero adicionado com sucesso!', 'success')
        return redirect(url_for('listar_generos'))
    return render_template('generos/cadastrar_genero.html', tabela='generos', dado=None)

# Editar Gêneros 
@app.route('/generos/editar/<int:id>', methods=['GET', 'POST'])
def editar_genero(id):
    with engine.connect() as conn:
        if request.method == 'POST':
            nome = request.form['nome']
            conn.execute(text("UPDATE generos SET nome_genero=:nome WHERE id_genero=:id"),
                         {"nome": nome, "id": id})
            conn.commit()
            flash('Gênero atualizado com sucesso!', 'success')
            return redirect(url_for('listar_generos'))

        genero = conn.execute(text("SELECT * FROM generos WHERE id_genero=:id"), {"id": id}).fetchone()
    return render_template('generos/editar_genero.html', tabela='generos', dado=genero)

# Excluir Gêneros 
@app.route('/generos/excluir/<int:id>')
def excluir_genero(id):
    with engine.connect() as conn:
        conn.execute(text("DELETE FROM generos WHERE id_genero=:id"), {"id": id})
        conn.commit()
    flash('Gênero excluído com sucesso!', 'success')
    return redirect(url_for('listar_generos'))

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

#---Usuários ---

# Listar Usuários
@app.route('/usuarios')
def listar_usuarios():
    with engine.connect() as conn:
        usuarios = conn.execute(text("SELECT id_usuario, nome_usuario, email, numero_telefone, data_inscricao, multa_atual FROM usuarios")).fetchall()
    return render_template('usuarios/listar_usuario.html', dados=usuarios, tabela='usuarios')

# Editar Usuários
@app.route('/usuarios/editar/<int:id>', methods=['GET', 'POST'])
def editar_usuario(id):
    with engine.connect() as conn:
        if request.method == 'POST':
            nome = request.form['nome']
            email = request.form['email']
            telefone = request.form['telefone']
            data = request.form['data_inscricao']
            multa = request.form['multa']
            conn.execute(text("""
                UPDATE usuarios
                SET nome_usuario=:nome, email=:email, numero_telefone=:telefone, data_inscricao=:data, multa_atual=:multa
                WHERE id_usuario=:id
            """), {"nome": nome, "email": email, "telefone": telefone, "data": data, "multa": multa, "id": id})
            conn.commit()
            flash('Usuário atualizado com sucesso!', 'success')
            return redirect(url_for('listar_usuarios'))

        usuario = conn.execute(text("SELECT * FROM usuarios WHERE id_usuario=:id"), {"id": id}).fetchone()
    return render_template('usuarios/editar_usuario.html', tabela='usuarios', dado=usuario)

# Excluir Usuários
@app.route('/usuarios/excluir/<int:id>')
def excluir_usuario(id):
    with engine.connect() as conn:
        conn.execute(text("DELETE FROM usuarios WHERE id_usuario=:id"), {"id": id})
        conn.commit()
    flash('Usuário excluído com sucesso!', 'success')
    return redirect(url_for('listar_usuarios'))

# Listar Livros
@app.route("/livros")
def listar_livros():
    with engine.connect() as conn:
        livros = conn.execute(text("""
            SELECT l.*, a.Nome_autor, g.nome_genero, e.Nome_editora 
            FROM Livros l
            LEFT JOIN Autores a ON l.Autor_id = a.ID_autor
            LEFT JOIN generos g ON l.Genero_id = g.id_genero
            LEFT JOIN Editoras e ON l.Editora_id = e.ID_editora
        """)).fetchall()
    return render_template("livros/listar_livro.html", livros=livros)

# Cadastrar Livros
@app.route("/livros/criar_livro", methods=["GET", "POST"])
def criar_livro():
    with engine.connect() as conn:
        autores = conn.execute(text("SELECT * FROM Autores")).fetchall()
        generos = conn.execute(text("SELECT * FROM generos")).fetchall()
        editoras = conn.execute(text("SELECT * FROM Editoras")).fetchall()
        
    if request.method == "POST":
        titulo = request.form.get("titulo")
        autor_id = request.form.get("autor_id")
        isbn = request.form.get("isbn")
        ano_publicacao = request.form.get("ano_publicacao")
        genero_id = request.form.get("genero_id")
        editora_id = request.form.get("editora_id")
        quantidade = request.form.get("quantidade")
        resumo = request.form.get("resumo")

        with engine.begin() as conn:
            conn.execute(
                text("""
                    INSERT INTO Livros 
                    (Titulo, Autor_id, ISBN, Ano_publicacao, Genero_id, Editora_id, Quantidade_disponivel, Resumo) 
                    VALUES (:titulo, :autor_id, :isbn, :ano_publicacao, :genero_id, :editora_id, :quantidade, :resumo)
                """),
                {
                    "titulo": titulo,
                    "autor_id": autor_id,
                    "isbn": isbn,
                    "ano_publicacao": ano_publicacao,
                    "genero_id": genero_id,
                    "editora_id": editora_id,
                    "quantidade": quantidade,
                    "resumo": resumo
                }
            )
        flash("Livro criado com sucesso!", "success")
        return redirect(url_for("listar_livros"))

    return render_template("livros/criar_livro.html", autores=autores, generos=generos, editoras=editoras)

# Editar Livros
@app.route("/livros/editar_livro/<int:id>", methods=["GET", "POST"])
def editar_livro(id):
    with engine.connect() as conn:
        livro = conn.execute(
            text("SELECT * FROM Livros WHERE ID_livro = :id"), {"id": id}
        ).fetchone()
        
        autores = conn.execute(text("SELECT * FROM Autores")).fetchall()
        generos = conn.execute(text("SELECT * FROM generos")).fetchall()
        editoras = conn.execute(text("SELECT * FROM Editoras")).fetchall()
    
    if not livro:
        flash("Livro não encontrado!", "error")
        return redirect(url_for("listar_livros"))

    if request.method == "POST":
        titulo = request.form.get("titulo")
        autor_id = request.form.get("autor_id")
        isbn = request.form.get("isbn")
        ano_publicacao = request.form.get("ano_publicacao")
        genero_id = request.form.get("genero_id")
        editora_id = request.form.get("editora_id")
        quantidade = request.form.get("quantidade")
        resumo = request.form.get("resumo")
        
        with engine.begin() as conn:
            conn.execute(
                text("""
                    UPDATE Livros
                    SET Titulo = :titulo,
                        Autor_id = :autor_id,
                        ISBN = :isbn,
                        Ano_publicacao = :ano_publicacao,
                        Genero_id = :genero_id,
                        Editora_id = :editora_id,
                        Quantidade_disponivel = :quantidade,
                        Resumo = :resumo
                    WHERE ID_livro = :id
                """),
                {
                    "titulo": titulo,
                    "autor_id": autor_id,
                    "isbn": isbn,
                    "ano_publicacao": ano_publicacao,
                    "genero_id": genero_id,
                    "editora_id": editora_id,
                    "quantidade": quantidade,
                    "resumo": resumo,
                    "id": id
                }
            )
        flash("Livro atualizado com sucesso!", "success")
        return redirect(url_for("listar_livros"))

    return render_template("livros/editar_livro.html", 
                         livro=livro, autores=autores, generos=generos, editoras=editoras)

# Excluir Livros
@app.route("/livros/excluir_livro/<int:id>")
def excluir_livro(id):
    with engine.begin() as conn:
        conn.execute(
            text("DELETE FROM Livros WHERE ID_livro = :id"),
            {"id": id}
        )
    flash("Livro excluído com sucesso!", "success")
    return redirect(url_for("listar_livros"))




