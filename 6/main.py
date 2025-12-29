import os
import sqlite3
from PIL import Image
import math

conn = sqlite3.connect("pencil.db")
cur = conn.cursor()
cur.execute("""
CREATE TABLE IF NOT EXISTS samples (
    id INTEGER PRIMARY KEY,
    l_mean REAL,
    l_std REAL,
    is_pencil INTEGER
)
""")
conn.commit()

def features(path):
    img = Image.open(path).convert("L").resize((256, 256))
    px = list(img.getdata())
    mean = sum(px) / len(px)
    std = math.sqrt(sum((p - mean) ** 2 for p in px) / len(px))
    return mean, std

base = "photo"

for name in os.listdir(base):
    if not name.lower().endswith(".png"):
        continue
    path = os.path.join(base, name)
    m, s = features(path)
    cur.execute(
        "INSERT INTO samples (l_mean, l_std, is_pencil) VALUES (?, ?, ?)",
        (m, s, 1)
    )

conn.commit()
conn.close()