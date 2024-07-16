import matplotlib.pyplot as plt
import numpy as np
from celluloid import Camera
from itertools import product
from matplotlib.colors import ListedColormap

cmap = ListedColormap([
    "white",        # 0
    "silver",       # 1
    "rosybrown",    # 2
    "yellow",       # 3
    "orange",       # 4
    "red",          # 5
    "green",        # 6
    "limegreen",    # 7
    "springgreen",  # 8
    "aquamarine"    # 9
])

def run(ca: np.ndarray, n: int, k: int, until: int):
    fig, ax = plt.subplots()
    camera = Camera(fig)
    kw = dict(cmap=cmap, origin="lower", vmin=0, vmax=9)
    ax.matshow(ca, **kw)
    camera.snap()

    nr, nc = ca.shape
    for _ in range(until):
        new_ca = ca.copy()
        for i, j in product(range(ca.shape[0]), range(ca.shape[1])):
            neighbors = (
                ca[(i-1) % nr,  (j-1) % nc],
                ca[(i-1) % nr,  j],
                ca[(i-1) % nr,  (j+1) % nc],
                ca[i,           (j+1) % nc],
                ca[(i+1) % nr,  (j+1) % nc],
                ca[(i+1) % nr,  j],
                ca[(i+1) % nr,  (j-1) % nc],
                ca[i,           (j-1) % nc]
            )
            new_ca[i, j] = apply_rule(ca[i, j], neighbors, n, k)
        ca = new_ca

        ax.matshow(ca, **kw)
        camera.snap()
    
    return (fig, ax), camera.animate()

def apply_rule(cell: int, neighbors: list, n: int, k: int):
    if 0 < cell <= n//2:
        return cell + 1
    elif cell > n//2:
        return (cell + 1) % n
    ill = 0
    for ni in neighbors:
        if 0 < ni <= n//2:
            ill += 1
    return int(ill >= k)

k, n = 5, 10
size = 101, 101
until = 200

rg = np.random.default_rng()
ca = rg.integers(0, 6, size, dtype=np.uint8)

(fig, ax), ani = run(ca, n, k, until)

ax.set_xticks([])
ax.set_yticks([])
ani.save(f"{__file__.split('.')[0]}_k{k}.gif", dpi=200)
