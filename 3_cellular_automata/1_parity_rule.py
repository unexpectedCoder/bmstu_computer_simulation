import matplotlib.pyplot as plt
from celluloid import Camera
from copy import deepcopy
from itertools import product


def create_ca(size: tuple):
    r, c = size
    ca = [
        [0 for _ in range(c)]
        for _ in range(r)
    ]
    ca[r//2][c//2] = 1
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
    new_ca = deepcopy(ca)
    rows, columns = range(len(ca)), range(len(ca[0]))
    for i, j in product(rows, columns):
        s = calc_neighbors(ca, (i, j))
        new_ca[i][j] = int(s % 2 != 0)
    return new_ca

def calc_neighbors(ca, cell):
    i, j = cell
    s = 0

    if 0 < i < len(ca) - 1:
        s += ca[i-1][j] + ca[i+1][j]
    elif i == 0:
        s += ca[i+1][j]
    else:
        s += ca[i-1][j]
    
    if 0 < j < len(ca[0]) - 1:
        s += ca[i][j-1] + ca[i][j+1]
    elif j == 0:
        s += ca[i][j+1]
    else:
        s += ca[i][j-1]
    
    return s

ca = create_ca(size=(51, 51))
(fig, ax), ani = run(ca, until=50)

ax.set_xticks([])
ax.set_yticks([])
ani.save("1_ca_parity_rule.gif", dpi=150)
