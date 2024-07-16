import matplotlib.pyplot as plt
import numpy as np
from celluloid import Camera
from copy import deepcopy
from itertools import product


def create_ca_1():
    ca = np.zeros((201, 201), dtype=np.int8)
    nr, nc = ca.shape
    cx, cy = nc // 2, nr // 2
    w, h = 7, 10

    ca[cy + h + 1, cx - w:cx + w + 1] = 1
    ca[cy + h, cx - w + 1:cx + w] = 1

    ca[cy - h - 1, cx - w:cx + w + 1] = 1
    ca[cy - h, cx - w + 1:cx + w] = 1

    ca[cy - h:cy + h + 1, cx - w - 1] = 1
    ca[cy - h + 1:cy + h, cx - w] = 1

    ca[cy - h:cy + h + 1, cx + w + 1] = 1
    ca[cy - h + 1:cy + h, cx + w] = 1

    return ca

def create_ca_2():
    ca = np.zeros((201, 201), dtype=np.int8)
    nr, nc = ca.shape
    cx, cy = nc // 2, nr // 2
    w, h = 7, 10
    ca[cy - h:cy + h + 1, cx - w:cx + w + 1] = 1
    return ca


def run(ca, until):
    fig, ax = plt.subplots()
    camera = Camera(fig)

    kw = dict(origin="lower", cmap="binary")
    ax.matshow(ca, **kw)
    camera.snap()
    for _ in range(until):
        ca = update(ca)
        ax.matshow(ca, **kw)
        camera.snap()
    
    return (fig, ax), camera.animate()

def update(ca):
    new_ca = ca.copy()
    m, n = ca.shape
    rows, columns = range(m), range(n)
    for i, j in product(rows, columns):
        s = calc_neighbors(ca, (i, j))
        new_ca[i, j] = int(s % 2 != 0)
    return new_ca

def calc_neighbors(ca, cell):
    i, j = cell
    s = 0

    if 0 < i < len(ca) - 1:
        s += ca[i-1, j] + ca[i+1, j]
    elif i == 0:
        s += ca[i+1, j]
    else:
        s += ca[i-1, j]
    
    if 0 < j < ca[0].size - 1:
        s += ca[i, j-1] + ca[i, j+1]
    elif j == 0:
        s += ca[i, j+1]
    else:
        s += ca[i, j-1]
    
    return s

ca = create_ca_2()
(fig, ax), ani = run(ca, until=200)

ax.set_xticks([])
ax.set_yticks([])
ani.save("2_ca_parity_rule_2.gif", dpi=150)
