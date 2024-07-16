import matplotlib.pyplot as plt
import numpy as np
from celluloid import Camera
from collections import namedtuple
from dataclasses import dataclass
from tqdm import trange

DIRECTION = np.array([
        [1, 1],
        [1, 0],
        [1, -1],
        [0, 1],
        [0, 0],
        [0, -1],
        [-1, 1],
        [-1, 0],
        [-1, -1]
    ])
LENCORR = np.array(
    [1/36, 1/9, 1/36, 1/9, 4/9, 1/9, 1/36, 1/9, 1/36]
)
COL_1 = np.array([0, 1, 2])
COL_2 = np.array([3, 4, 5])
COL_3 = np.array([6, 7, 8])

# "_lb" означает "в ед. решётки"
LBEParams = namedtuple(
    "LBEParams",
    "Re nx ny u_lb p_inf rho_inf"
)

Viscosity = namedtuple(
    "Viscosity", " nu_lb omega"
)

@dataclass(frozen=True)
class Obstacle:
    radius: float
    cx: float
    cy: float

    def where(self, nx: int, ny: int):
        f = lambda x, y: (x - self.cx)**2 + (y - self.cy)**2 < self.radius**2
        return np.fromfunction(f, (nx, ny))

def solve(par: LBEParams,
          obs: Obstacle,
          visc: Viscosity,
          until: int,
          visualize_every: int):
    fig1, ax1 = plt.subplots()
    fig2, ax2 = plt.subplots()
    fig3, ax3 = plt.subplots()
    camera1 = Camera(fig1)
    camera2 = Camera(fig2)
    camera3 = Camera(fig3)
    imshow_kw = dict(
        cmap="viridis", origin="lower", interpolation="bicubic"
    )
    ax1.set_title(r"Скорость $\|\mathbf{u}\|$")
    ax2.set_title(r"Давление $p$")
    ax3.set_title(r"Плотность $\mathrm{\rho}$")

    lattice_shape = par.nx, par.ny
    ly = par.ny - 1
    where_obs = obs.where(par.nx, par.ny)
    init_velo = lambda d, x, y: \
        (1 - d)*par.u_lb*(1 + 1e-4*np.sin(2*np.pi * y/ly))
    v_initial = np.fromfunction(init_velo, (2, par.nx, par.ny))

    fin = calc_equilibrium(par.rho_inf, v_initial, lattice_shape)
    for t in trange(until):
        # Правая стенка - условие выхода (outflow)
        fin[COL_3, -1, :] = fin[COL_3, -2, :]
        # Расчёт макроскопических величин: плотности, скорости, давления
        rho, u, p = calc_macroscopic(fin, lattice_shape)

        # Визуализация
        speed = np.sqrt(u[0]**2 + u[1]**2)
        if t % visualize_every == 0:
            ax1.imshow(speed.T, **imshow_kw)
            camera1.snap()
            ax2.imshow(p.T, **imshow_kw)
            camera2.snap()
            ax3.imshow(rho.T, **imshow_kw)
            camera3.snap()

        # Левая стенка - условие входа (inflow)
        u[:, 0, :] = v_initial[:, 0, :]
        rho[0, :] = \
            1/(1 - u[0, 0, :]) * (
                fin[COL_2, 0, :].sum(axis=0) \
                + 2*fin[COL_3, 0, :].sum(axis=0)
            )
        # Релаксация
        feq = calc_equilibrium(rho, u, lattice_shape)
        fin[[0, 1, 2], 0, :] = \
            feq[[0, 1, 2], 0, :] \
            + fin[[8, 7, 6], 0, :] \
            - feq[[8, 7, 6], 0, :]
        # Столкновения
        fout = fin - visc.omega * (fin - feq)
        # Отражение от преграды
        for i in range(9):
            fout[i, where_obs] = fin[8 - i, where_obs]
        # Распространение
        for i in range(9):
            fin[i] = np.roll(fout[i], DIRECTION[i], axis=(0, 1))
    
    return (
        ((fig1, ax1), (fig2, ax2), (fig3, ax3)),
        (camera1.animate(), camera2.animate(), camera3.animate())
    )

def calc_equilibrium(rho: np.ndarray, u: np.ndarray, lattice_shape: tuple):
    u_sqr = 1.5*(u[0]**2 + u[1]**2)
    feq = np.zeros((9, *lattice_shape), dtype=float)
    for i in range(9):
        cu = 3 * (
            DIRECTION[i, 0] * u[0, :, :] \
            + DIRECTION[i, 1] * u[1, :, :]
        )
        feq[i, :, :] = rho * LENCORR[i] * (
            1 + cu + 0.5 * cu**2 - u_sqr
        )
    return feq

def calc_macroscopic(fin: np.ndarray, lattice_shape: tuple):
    rho = fin.sum(axis=0)
    u_sum = np.zeros((2, *lattice_shape), dtype=float)
    for i in range(9):
        u_sum[0, :, :] += DIRECTION[i, 0] * fin[i, :, :]
        u_sum[1, :, :] += DIRECTION[i, 1] * fin[i, :, :]
    p = rho / 3
    return rho, u_sum / rho, p

par = LBEParams(180, 420, 180, 0.01, 1e5, 1.2)
obs = Obstacle(par.ny // 9, par.nx // 4, par.ny // 2)
nu_lb = par.u_lb * obs.radius / par.Re
visc = Viscosity(nu_lb, 1 / (3 * nu_lb + 0.5))

_, (ani1, ani2, ani3) = solve(
    par, obs, visc, until=10_000, visualize_every=200
)

ani1.save(
    f"{__file__.split('.')[0]}_speed_Re{int(par.Re)}.gif", fps=25, dpi=200
)
ani2.save(
    f"{__file__.split('.')[0]}_pressure_Re{int(par.Re)}.gif", fps=25, dpi=200
)
ani3.save(
    f"{__file__.split('.')[0]}_density_Re{int(par.Re)}.gif", fps=25, dpi=200
)
