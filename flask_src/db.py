import os
from pathlib import Path
import mysql.connector
from dotenv import load_dotenv

load_dotenv()


def conectar():
    """Abre e retorna uma conexão com o banco MySQL (Aiven)."""
    try:
        ssl_ca = os.getenv("SSL_CA")
        ssl_path = str(Path(__file__).parent / ssl_ca) if ssl_ca else None

        params = dict(
            host=os.getenv("DB_HOST"),
            port=int(os.getenv("DB_PORT", 3306)),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            database=os.getenv("DB_NAME"),
            connection_timeout=30,
            autocommit=False,
        )

        if ssl_path:
            params["ssl_disabled"] = False
            params["ssl_ca"] = ssl_path

        conn = mysql.connector.connect(**params)
        conn.ping(reconnect=True, attempts=3, delay=2)
        return conn

    except mysql.connector.Error as erro:
        print(f"❌ Erro ao conectar ao banco: {erro}")
        return None


if __name__ == "__main__":
    conn = conectar()
    if conn:
        print("✅ Conectado com sucesso!")
        conn.close()
