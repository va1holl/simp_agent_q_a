import sqlite3

conn = sqlite3.connect("t9.db")
cur = conn.cursor()
cur.execute("CREATE TABLE IF NOT EXISTS bigrams (w1 TEXT, w2 TEXT, cnt INTEGER, PRIMARY KEY (w1, w2))")

def train(tokens):
    for i in range(len(tokens) - 1):
        w1 = tokens[i]
        w2 = tokens[i + 1]
        cur.execute("SELECT cnt FROM bigrams WHERE w1=? AND w2=?", (w1, w2))
        row = cur.fetchone()
        if row:
            cur.execute("UPDATE bigrams SET cnt=? WHERE w1=? AND w2=?", (row[0] + 1, w1, w2))
        else:
            cur.execute("INSERT INTO bigrams (w1, w2, cnt) VALUES (?, ?, ?)", (w1, w2, 1))
    conn.commit()

def suggest_next(word):
    cur.execute("SELECT w2 FROM bigrams WHERE w1=? ORDER BY cnt DESC LIMIT 1", (word,))
    row = cur.fetchone()
    if row:
        return row[0]
    return None

try:
    while True:
        line = input().strip()
        if not line:
            break
        tokens = line.split()
        train(tokens)
        last = tokens[-1]
        nxt = suggest_next(last)
        if nxt:
            print(line + " " + nxt)
        else:
            print(line)
finally:
    conn.close()