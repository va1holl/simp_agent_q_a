import psycopg2
from psycopg2.extras import RealDictCursor

DB_CONFIG = {
    "dbname": "agent_q_a",
    "user": "postgres",
    "password": r'b3e<a4Yxm$nz(\l(pd0Z',
    "host": "localhost",
    "port": 5432,
}


def get_connection():
    conn = psycopg2.connect(**DB_CONFIG)
    conn.autocommit = True
    return conn


def init_db(conn):
    with conn.cursor() as cur:
        cur.execute("""
            CREATE TABLE IF NOT EXISTS question (
                id SERIAL PRIMARY KEY,
                text TEXT UNIQUE NOT NULL
            );
        """)

        cur.execute("""
            CREATE TABLE IF NOT EXISTS answer (
                id SERIAL PRIMARY KEY,
                question_id INTEGER NOT NULL REFERENCES question(id) ON DELETE CASCADE,
                text TEXT NOT NULL,
                rating_sum INTEGER NOT NULL DEFAULT 0,
                rating_cnt INTEGER NOT NULL DEFAULT 0,
                created_at TIMESTAMP NOT NULL DEFAULT NOW()
            );
        """)


def get_or_create_question(conn, text: str) -> int:
    with conn.cursor(cursor_factory=RealDictCursor) as cur:
        cur.execute("SELECT id FROM question WHERE text = %s;", (text,))
        row = cur.fetchone()
        if row:
            return row["id"]

        cur.execute(
            "INSERT INTO question (text) VALUES (%s) RETURNING id;",
            (text,),
        )
        return cur.fetchone()["id"]


def get_answers(conn, question_id: int):
    with conn.cursor(cursor_factory=RealDictCursor) as cur:
        cur.execute("""
            SELECT id, text, rating_sum, rating_cnt
            FROM answer
            WHERE question_id = %s
            ORDER BY created_at ASC;
        """, (question_id,))
        return cur.fetchall()


def create_answer(conn, question_id: int, text: str) -> int:
    with conn.cursor(cursor_factory=RealDictCursor) as cur:
        cur.execute("""
            INSERT INTO answer (question_id, text)
            VALUES (%s, %s)
            RETURNING id;
        """, (question_id, text))
        return cur.fetchone()["id"]


def update_answer_rating(conn, answer_id: int, rating: int):
    with conn.cursor() as cur:
        cur.execute("""
            UPDATE answer
            SET rating_sum = rating_sum + %s,
                rating_cnt = rating_cnt + 1
            WHERE id = %s;
        """, (rating, answer_id))