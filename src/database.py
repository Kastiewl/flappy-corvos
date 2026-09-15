import sqlite3
from pathlib import Path

# Caminho absoluto para salvar o arquivo de banco na raiz do projeto
DB_PATH = Path(__file__).resolve().parent.parent / "ranking.db"


def get_connection() -> sqlite3.Connection:
    """Retorna uma conexão ativa com o banco SQLite."""
    return sqlite3.connect(DB_PATH)


def init_db() -> None:
    """Cria a tabela de pontuações caso ela ainda não exista."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS scores (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                score INTEGER NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP            
            );
            """
        )
        conn.commit()


def save_score(score: int) -> None:
    """Registra uma nova pontuação no histórico"""
    if score <= 0:
        return
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO scores (score) VALUES (?);",
            (score,),
        )
        conn.commit()


def get_high_score() -> int:
    """Retorna o maior recorde registrado ou 0 se a tabela estiver vazia"""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT MAX (score) FROM scores;")
        result = cursor.fetchone()
        return result[0] if result and result[0] is not None else 0


def get_top_scores(limit: int = 5) -> list[int]:
    """Retorna as melhores pontuações para a futura tela do ranking."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT score FROM scores ORDER BY score DESC LIMIT?;",
            (limit,),
        )
        return [row[0] for row in cursor.fetchall()]