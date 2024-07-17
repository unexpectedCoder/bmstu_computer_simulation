import matplotlib.pyplot as plt
import numpy as np
from celluloid import Camera
from tqdm import trange

DIRECTION_EVEN = np.array([
    (1, 0),
    (1, 1),
    (0, 1),
    (-1, 0),
    (0, -1),
    (1, -1)
])
DIRECTION_ODD = np.array([
    (1, 0),
    (0, 1),
    (-1, 1),
    (-1, 0),
    (-1, -1),
    (0, -1)
])
REFLECTION = {
    0: 3,
    1: 4,
    2: 5,
    3: 0,
    4: 1,
    5: 2
}

DENSITY = 0.2
M, N = 200, 200
SIDE = 40
SHIFT = 0
CX, CY = M//2 + int(SHIFT*SIDE), N//2 + int(SHIFT*SIDE)

SCATTER_KW = dict(
    cmap="cividis", vmin=0, vmax=6, s=5, marker="h"
)
RG = np.random.default_rng()

def create_lattice_rect():
    lattice = RG.random((6, M, N)) < DENSITY
    lattice[:, CY - SIDE//2:CY + SIDE//2 + 1, CX - SIDE:CX + SIDE + 1] = False
    return lattice

def create_lattice_sphere():
    lattice = RG.random((6, M, N)) < DENSITY
    i, j = np.indices((M, N))
    lattice = np.where((i - CY)**2 + (j - CX)**2 < (SIDE//2)**2, True, lattice)
    return lattice

def run(lattice: np.ndarray, until: int):
    fig, ax = plt.subplots()
    camera = Camera(fig)

    x, y = np.meshgrid(np.arange(N, dtype=float), np.arange(M, dtype=float))
    x[1::2] += 0.5
    c = lattice.sum(axis=0)
    ax.scatter(x, y, c=c, **SCATTER_KW)
    camera.snap()

    s = lattice.sum()
    for t in trange(until):
        lattice = update(lattice)
        assert(s == lattice.sum())

        if t % 2 == 0:
            ax.scatter(x, y, c=lattice.sum(axis=0), **SCATTER_KW)
            camera.snap()
    
    return (fig, ax), camera.animate()

def update(n_in: np.ndarray):
    n_out = np.zeros_like(n_in)

    # Столкновения:
    # - две частицы
    coll2_03 = n_in[0] & n_in[3] & (
        ~(n_in[1] | n_in[2] | n_in[4] | n_in[5])
    )
    coll2_14 = n_in[1] & n_in[4] & (
        ~(n_in[0] | n_in[2] | n_in[3] | n_in[5])
    )
    coll2_25 = n_in[2] & n_in[5] & (
        ~(n_in[0] | n_in[1] | n_in[3] | n_in[4])
    )
    dissipation = 1, 2
    s = RG.choice(dissipation)
    n_out[0 + s, coll2_03] = True
    n_out[3 + s, coll2_03] = True
    s = RG.choice(dissipation)
    n_out[1 + s, coll2_14] = True
    n_out[(4 + s)%6, coll2_14] = True
    s = RG.choice(dissipation)
    n_out[2 + s, coll2_25] = True
    n_out[(5 + s)%6, coll2_25] = True
    
    # - три частицы
    coll3_024 = n_in[0] & n_in[2] & n_in[4] & (
        ~(n_in[1] | n_in[3] | n_in[5])
    )
    n_out[1, coll3_024] = True
    n_out[3, coll3_024] = True
    n_out[5, coll3_024] = True

    coll3_135 = n_in[1] & n_in[3] & n_in[5] & (
        ~(n_in[0] | n_in[2] | n_in[4])
    )
    n_out[0, coll3_135] = True
    n_out[2, coll3_135] = True
    n_out[4, coll3_135] = True

    # - четыре частицы
    coll4_0134 = n_in[0] & n_in[1] & n_in[3] & n_in[4] & (
        ~(n_in[2] | n_in[5])
    )
    n_out[0, coll4_0134] = True
    n_out[3, coll4_0134] = True
    n_out[2, coll4_0134] = True
    n_out[5, coll4_0134] = True

    coll4_1245 = n_in[1] & n_in[2] & n_in[4] & n_in[5] & (
        ~(n_in[0] | n_in[3])
    )
    n_out[1, coll4_1245] = True
    n_out[2, coll4_1245] = True
    n_out[4, coll4_1245] = True
    n_out[5, coll4_1245] = True

    coll4_0235 = n_in[0] & n_in[2] & n_in[3] & n_in[5] & (
        ~(n_in[1] | n_in[4])
    )
    n_out[0, coll4_0235] = True
    n_out[1, coll4_0235] = True
    n_out[3, coll4_0235] = True
    n_out[4, coll4_0235] = True

    without_coll = ~(
        coll2_03 | coll2_14 | coll2_25
        | coll3_024 | coll3_135
        | coll4_0134 | coll4_0235 | coll4_1245
    )
    n_out[:, without_coll] = n_in[:, without_coll]

    # Распространение
    lattice = np.zeros_like(n_in)
    rows, cols = lattice.shape[1:]
    for i in range(lattice.shape[0]):
        for r in range(lattice.shape[1]):
            d = DIRECTION_EVEN[i] if r % 2 == 0 else DIRECTION_ODD[i]
            for c in range(lattice.shape[2]):
                if n_out[i, r, c]:
                    r_new, c_new = r + d[1], c + d[0]

                    # Проверка границ
                    if r_new == -1 or r_new == rows or c_new == -1 or c_new == cols:
                        # Отражение
                        lattice[REFLECTION[i], r, c] = True
                    else:
                        lattice[i, r_new, c_new] = True
    
    return lattice

# lattice = create_lattice_rect()
lattice = create_lattice_sphere()

(fig, ax), ani = run(lattice, until=500)
ax.set(xticks=[], yticks=[], aspect="equal")

ani.save(f"{__file__.split('.')[0]}.gif", fps=25, dpi=150)
# plt.show()
