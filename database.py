from sqlalchemy import create_engine, text

# --- Configuração do banco já existente ---
user = "root"
password = "felipe"
host = "localhost"
port = 3307
database = "db_biblioteca"

# Montando a URL corretamente com porta
engine = create_engine(f"mysql+pymysql://{user}:{password}@{host}:{port}/{database}")

# --- Criação das tabelas ---
with engine.connect() as conn:
    conn.execute(text("""
        CREATE TABLE IF NOT EXISTS Autores (
            ID_autor INT AUTO_INCREMENT PRIMARY KEY,
            Nome_autor VARCHAR(255) NOT NULL,
            Nacionalidade VARCHAR(255),
            Data_nascimento DATE,
            Biografia TEXT
        )
    """))

    conn.execute(text("""
        CREATE TABLE IF NOT EXISTS Editoras (
            ID_editora INT AUTO_INCREMENT PRIMARY KEY,
            Nome_editora VARCHAR(255) NOT NULL,
            Endereco_editora TEXT
        )
    """))

    print("Tabelas criadas ou já existiam.")
