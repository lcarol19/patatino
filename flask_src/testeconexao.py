import sys
import subprocess

# Função para instalar pacote caso não exista
def instalar_pacote(pacote):
    try:
        subprocess.check_call(
            [sys.executable, "-m", "pip", "install", pacote]
        )
        print(f"✅ Pacote '{pacote}' instalado com sucesso.")
    except Exception as erro:
        print(f"❌ Erro ao instalar '{pacote}': {erro}")
        sys.exit(1)

# Verifica e instala python-dotenv
try:
    from dotenv import load_dotenv
except ImportError:
    print("⚠️ python-dotenv não encontrado. Instalando...")
    instalar_pacote("python-dotenv")
    from dotenv import load_dotenv

# Verifica e instala mysql-connector-python
try:
    import mysql.connector
except ImportError:
    print("⚠️ mysql-connector-python não encontrado. Instalando...")
    instalar_pacote("mysql-connector-python")
    import mysql.connector

import os

# Carrega o .env
load_dotenv()

try:
    conexao = mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        port=int(os.getenv("DB_PORT")),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME"),
        ssl_ca=os.getenv("SSL_CA")
    )

    print("✅ Conexão realizada com sucesso!")

    cursor = conexao.cursor()
    cursor.execute("SELECT VERSION()")

    versao = cursor.fetchone()

    print(f"Versão do MySQL: {versao[0]}")
    print(f"Host: {os.getenv('DB_HOST')}")
    print(f"Banco: {os.getenv('DB_NAME')}")

    cursor.execute("DESCRIBE fotos_animais")

    colunas = cursor.fetchall()

    print("\n=== ESTRUTURA REAL DE fotos_animais ===")
    for coluna in colunas:
        print(coluna)

    cursor.execute("DESCRIBE fotos_animais")

    colunas = cursor.fetchall()

    print("\n=== ESTRUTURA DA TABELA fotos_animais ===")
    for coluna in colunas:
        print(coluna)


    cursor.close()
    conexao.close()
except Exception as erro:
    print(f"❌ Erro na conexão: {erro}")