import tkinter as tk
import random

SIZE = 256
CELL = 2

field = [[random.randint(0, 1) for _ in range(SIZE)] for _ in range(SIZE)]


def step():
    new = [[0]*SIZE for _ in range(SIZE)]
    for y in range(1, SIZE-1):
        for x in range(1, SIZE-1):
            s = 0
            for dy in (-1, 0, 1):
                for dx in (-1, 0, 1):
                    s += field[y+dy][x+dx]
            new[y][x] = 1 if s >= 5 else 0
    for y in range(SIZE):
        for x in range(SIZE):
            field[y][x] = new[y][x]
    draw()
    root.after(50, step)


def draw():
    canvas.delete("all")
    for y in range(SIZE):
        for x in range(SIZE):
            if field[y][x]:
                canvas.create_rectangle(
                    x*CELL, y*CELL,
                    x*CELL+CELL, y*CELL+CELL,
                    fill="black", outline=""
                )


root = tk.Tk()
canvas = tk.Canvas(root, width=SIZE*CELL, height=SIZE*CELL, bg="white")
canvas.pack()

draw()
step()
root.mainloop()