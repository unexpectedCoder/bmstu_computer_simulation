import matplotlib.pyplot as plt
import numpy as np

VX_LIST = [1, -1, 0, 0, 0]
VY_LIST = [0, 0, 0, -1, 1]

def random_walk(n_particles, nx, ny, dt, until):
    x, y = np.full(n_particles, nx//2), np.full(n_particles, ny//2)
    history = np.zeros((nx, ny))
    t = 0

    while t < until + dt:
        vx, vy = random_v(n_particles)
        x = (x + vx) % nx
        y = (y + vy) % ny
        t += dt
        for i in range(n_particles):
            history[x[i], y[i]] += 1
    
    return history

def random_v(n):
    return (
        np.random.choice(VX_LIST, n),
        np.random.choice(VY_LIST, n)
    )

nx, ny = 101, 101
history = random_walk(100_000, nx, ny, 1, 1000)

x, y = np.linspace(-10, 10, nx), np.linspace(-10, 10, ny)
fig, ax = plt.subplots()
img = ax.contourf(x, y, history)
fig.colorbar(img, label="Численность")
ax.set(xlabel="$x$", ylabel="$y$", aspect="equal")

fig.savefig(f"{__file__.split('.')[0]}.png", dpi=300)
# plt.show()
