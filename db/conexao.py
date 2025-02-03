import mysql.connector
from mysql.connector import Error

def conectar_com_banco():
    try:
        conexao = mysql.connector.connect(
            host="autorack.proxy.rlwy.net",
            user="root",
            password="kQFyzyJcZRnjMirSCYZwhGivBQPegkbG",
            database="railway",
            port=25273
        )
        if conexao.is_connected():
            print('Conectado ao banco de dados')
            return conexao
    except Error as e:
        print(f"Erro ao conectar ao banco de dados: {e}")
        return None

def fechar_banco(conexao):
    if conexao and conexao.is_connected():
        conexao.close()

def tabela_empresa(conexao):
    cursor = conexao.cursor()

    cursor.execute(""" 
        CREATE TABLE IF NOT EXISTS empresas (
            id INT AUTO_INCREMENT PRIMARY KEY,
            cnpj VARCHAR(20) ,
            razao_social VARCHAR(255),
            user VARCHAR(255),
            data_cadastro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    conexao.commit()
    cursor.close()

def tabela_usuario(conexao):
    cursor = conexao.cursor()

    cursor.execute(""" 
        CREATE TABLE IF NOT EXISTS user (
            id INT AUTO_INCREMENT PRIMARY KEY,
            nome VARCHAR(255),
            senha VARCHAR(255),
            data_cadastro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)
    
    conexao.commit()
    cursor.close()

def criar_tabela(conexao):
    try:
        cursor = conexao.cursor()

        # Construção dinâmica do SQL com ou sem a coluna "Mês"
        create_table_query = f"""
        CREATE TABLE IF NOT EXISTS balancete_mensal (
            id INT AUTO_INCREMENT PRIMARY KEY,
            Conta VARCHAR(255),
            Descrição VARCHAR(255),
            `Saldo Anterior` VARCHAR(255),
            Débitos VARCHAR(255),
            Créditos VARCHAR(255),
            `Saldo Atual` VARCHAR(255),
            empresa VARCHAR(255),
            periodo VARCHAR(255),
            Usuario VARCHAR(255) DEFAULT '',
            `Data de Envio` TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """

        cursor.execute(create_table_query)
        conexao.commit()
        # print(f"Tabela 'balancete_mensal' criada ou já existe.")
    except mysql.connector.Error as e:
        erro = str(e)
        # print(f"Erro ao criar a tabela: {e}")
    finally:
        cursor.close()
    
def tabela_slide(conexao):
    cursor = conexao.cursor()

    cursor.execute(""" 
        CREATE TABLE IF NOT EXISTS slides (
            id INT AUTO_INCREMENT PRIMARY KEY,
            nome VARCHAR(255) not null,
            id_empresa int,
            FOREIGN KEY (id_empresa) REFERENCES empresas(id)
        );
    """)
    
    conexao.commit()
    cursor.close()

def codigos_slide(conexao):
    cursor = conexao.cursor()

    cursor.execute(""" 
        CREATE TABLE IF NOT EXISTS slide_codigos (
            id INT AUTO_INCREMENT PRIMARY KEY,
            slide_id INT,
            codigo VARCHAR(255) not null,
            `Data de Envio` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (slide_id) REFERENCES slides(id) ON DELETE CASCADE
        );
    """)
    
    conexao.commit()
    cursor.close()