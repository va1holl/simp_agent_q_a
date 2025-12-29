from PIL import Image
import os
import math

PLANETS = {}

def load_planet(name, path):
    img = Image.open(path).convert("L").resize((256, 256))
    PLANETS[name] = img.histogram()

def similarity(h1, h2):
    s = 0
    for a, b in zip(h1, h2):
        s += (a - b) ** 2
    return 100 / (1 + math.sqrt(s))

def recognize(path):
    img = Image.open(path).convert("L").resize((256, 256))
    h = img.histogram()
    best_name = None
    best_score = 0
    for name, ph in PLANETS.items():
        score = similarity(h, ph)
        if score > best_score:
            best_score = score
            best_name = name
    if best_score < 50:
        print("Неизвестная планета,", round(best_score, 2), "%")
        name = input("Введи имя планеты: ").strip()
        if name:
            PLANETS[name] = h
    else:
        print(best_name, round(best_score, 2), "%")

load_planet("Mars", "photo/mars.png")
load_planet("Jupiter", "photo/jupiter.png")
load_planet("Venus", "photo/venus.png")
load_planet("Saturn", "photo/saturn.png")
load_planet("Earth", "photo/earth.png")

while True:
    p = input("Путь к фото: ").strip()
    if not p:
        break
    recognize(p)
