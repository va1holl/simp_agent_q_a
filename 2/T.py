WIDTH = 256
HEIGHT = 256
BACKGROUND = 0
FOREGROUND = 1
BLOCK = 5

canvas = [[BACKGROUND for _ in range(WIDTH)] for _ in range(HEIGHT)]

T_BLOCK_W = 5
T_BLOCK_H = 5
T_W = T_BLOCK_W * BLOCK
T_H = T_BLOCK_H * BLOCK

template = [[BACKGROUND for _ in range(T_W)] for _ in range(T_H)]

def draw_t(target, ox, oy):
    for by in range(T_BLOCK_H):
        for bx in range(T_BLOCK_W):
            on = by == 0 or bx == 2
            if on:
                py = oy + by * BLOCK
                px = ox + bx * BLOCK
                for i in range(BLOCK):
                    for j in range(BLOCK):
                        target[py + i][px + j] = FOREGROUND

draw_t(template, 0, 0)
draw_t(canvas, 100, 80)

def match_at(x, y):
    for i in range(T_H):
        for j in range(T_W):
            if canvas[y + i][x + j] != template[i][j]:
                return False
    return True

found = False
for y in range(HEIGHT - T_H + 1):
    for x in range(WIDTH - T_W + 1):
        if match_at(x, y):
            found = True
            break
    if found:
        break

print("T found" if found else "T not found")
