import matplotlib.pyplot as plt
import numpy as np

def solve(dx_dy: tuple[float, float],
          T0: np.ndarray,
          dif: float,
          until: float):
    dx, dy = dx_dy
    
    dt = 0.1 * min(dx, dy)**2 / dif
    t, T = 0, T0
    while t < until + dt:
        T_right = np.roll(T, -1, axis=1)
        T_right[-1, :] = 0
        T_left = np.roll(T, 1, axis=1)
        T_left[:, 0] = 0
        T_up = np.roll(T, -1, axis=0)
        T_up[-1, :] = 0
        T_down = np.roll(T, 1, axis=0)
        T_down[0, :] = 0

        T += dif * dt * (
            (T_right - 2*T + T_left) / dx**2
            + (T_up - 2*T + T_down) / dy**2
        )

        t += dt

    return t, T

# Подготовка исходных данных
x, dx = np.linspace(-10, 10, 301, retstep=True)
y, dy = np.linspace(-10, 10, 301, retstep=True)
dif = 1
T0 = np.zeros((y.size, x.size))
T0[T0.shape[0]//2, T0.shape[1]//2] = 2700
grid = np.meshgrid(x, y)

# Решение
t, T = solve((dx, dy), T0, dif, until=1)

# Визуализация
fig, ax = plt.subplots()

x, y = grid
img = ax.contourf(x, y, T)
ax.set(xlabel="$x$", ylabel="$y$", aspect="equal")
fig.colorbar(img, ax=ax, shrink=0.92, label="$T$")

# Сохранение
fig.savefig(f"{__file__.split('.')[0]}.png", dpi=300)
# plt.show()
