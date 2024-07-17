import matplotlib.pyplot as plt
import numpy as np
from celluloid import Camera
from tqdm import trange

DIRECTION = np.array([
    [1, 0],
    [0, 1],
    [-1, 0],
    [0, -1]
])

DENSITY = 0.2
M, N = 201, 201
SHIFT = 0
SIDE = 40
CX, CY = M//2 + int(SHIFT*SIDE), N//2 + int(SHIFT*SIDE)

MATSHOW_KW = dict(
    cmap="cividis", origin="lower", vmin=0, vmax=4
)
RG = np.random.default_rng()

def create_lattice_rect():
    lattice = RG.random((4, M, N)) < DENSITY
    lattice[:, CY - SIDE//2:CY + SIDE//2 + 1, CX - SIDE:CX + SIDE + 1] = False
    return lattice

def create_lattice_sphere():
    lattice = RG.random((4, M, N)) < DENSITY
    i, j = np.indices((M, N))
    lattice = np.where((i - CY)**2 + (j - CX)**2 < (SIDE//2)**2, True, lattice)
    return lattice

def run(lattice: np.ndarray, until: int):
    fig, ax = plt.subplots()
    camera = Camera(fig)

    ax.matshow(lattice.sum(axis=0), **MATSHOW_KW)
    camera.snap()

    s = lattice.sum()
    for t in trange(until):
        lattice = update(lattice)
        assert(s == lattice.sum())

        if t % 2 == 0:
            ax.matshow(lattice.sum(axis=0), **MATSHOW_KW)
            camera.snap()
    
    return (fig, ax), camera.animate()

def update(n_in: np.ndarray):
    h_collision = n_in[0] & n_in[2] & (~(n_in[1] | n_in[3]))
    v_collision = n_in[1] & n_in[3] & (~(n_in[0] | n_in[2]))

    n_out = n_in.copy()
    n_out[0, h_collision], n_out[2, h_collision] = False, False
    n_out[1, v_collision], n_out[3, v_collision] = False, False
    n_out[0, v_collision], n_out[2, v_collision] = True, True
    n_out[1, h_collision], n_out[3, h_collision] = True, True

    for i in range(4):
        n_in[i] = np.roll(n_out[i], DIRECTION[i], axis=(1, 0))
    
    n_in[0, :, 0] = n_out[2, :, 0]
    n_in[1, 0, :] = n_out[3, 0, :]
    n_in[2, :, -1] = n_out[0, :, -1]
    n_in[3, -1, :] = n_out[1, -1, :]
    
    return n_in

# ca = create_lattice_rect()
ca = create_lattice_sphere()

(fig, ax), ani = run(ca, until=500)

ax.set_xticks([])
ax.set_yticks([])

ani.save(f"{__file__.split('.')[0]}.gif", fps=25, dpi=150)
# plt.show()
