import matplotlib.pyplot as plt
import numpy as np
from celluloid import Camera

DIRECTION = np.array([
    [1, 0],
    [0, 1],
    [-1, 0],
    [0, -1]
])
M, N = 201, 201
HOLE_H, HOLE_W = 30, 10
HOLE_X, HOLE_Y = N // 4, M // 2
DENSITY = 0.8
RG = np.random.default_rng()

def create_lattice():
    obstacle = np.fromfunction(create_obstacles, (M, N))
    lattice = RG.random((4, M, N)) < (1 - DENSITY)
    lattice[:, obstacle] = False
    lattice[:, :, :HOLE_X] = RG.random((4, M, HOLE_X)) < DENSITY
    return lattice, obstacle

def create_obstacles(y, x):
    cx, cy = HOLE_X, HOLE_Y
    h, w = HOLE_H//2, HOLE_W//2
    return ((y < cy - h) | (y > cy + h)) & ((cx <= x) & (x < cx + w))

def run(lattice: np.ndarray, obstacle: np.ndarray, until: int):
    fig, ax = plt.subplots()
    camera = Camera(fig)
    kw = dict(
        cmap="copper", origin="lower", vmin=0, vmax=4, interpolation="bilinear"
    )
    ax.matshow(lattice.sum(axis=0), **kw)
    camera.snap()
    
    s = lattice.sum()
    for t in range(until):
        lattice = update(lattice, obstacle)
        assert(s == lattice.sum())

        if t % 2 == 0:
            ax.matshow(lattice.sum(axis=0), **kw)
            camera.snap()
    
    return (fig, ax), camera.animate()

def update(n_in: np.ndarray, obstacle: np.ndarray):
    h_collision = n_in[0] & n_in[2] & (~(n_in[1] | n_in[3]))
    v_collision = n_in[1] & n_in[3] & (~(n_in[0] | n_in[2]))

    n_out = n_in.copy()
    n_out[0, h_collision], n_out[2, h_collision] = False, False
    n_out[1, v_collision], n_out[3, v_collision] = False, False
    n_out[0, v_collision], n_out[2, v_collision] = True, True
    n_out[1, h_collision], n_out[3, h_collision] = True, True

    for i in range(4):
        n_in[i] = np.roll(n_out[i], DIRECTION[i], axis=(1, 0))

    for i in range(4):
        hits = np.roll(obstacle, -DIRECTION[i], axis=(1, 0))
        n_in[(i + 2)%4, hits] = n_out[i, hits]
        n_in[i, obstacle] = False
    
    n_in[0, :, 0] = n_out[2, :, 0]
    n_in[1, 0, :] = n_out[3, 0, :]
    n_in[2, :, -1] = n_out[0, :, -1]
    n_in[3, -1, :] = n_out[1, -1, :]
    
    return n_in

lattice, obstacle = create_lattice()
until = 1000
(fig, ax), ani = run(lattice, obstacle, until)

ax.set_xticks([])
ax.set_yticks([])

ani.save(f"{__file__.split('.')[0]}.gif", fps=25, dpi=150)
