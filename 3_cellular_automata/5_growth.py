import numpy as np
import matplotlib.pyplot as plt
from celluloid import Camera

fig, ax = plt.subplots()
camera = Camera(fig)

# Parameters
width, height = 200, 200  # Grid size
Du, Dv = 0.16, 0.08       # Diffusion coefficients for U and V
F, k = 0.035, 0.065       # Feed rate and kill rate
dx, dt = 1.0, 1.0         # Grid spacing and time step


def laplacian(Z):
    return (
        -4 * Z
        + np.roll(Z, (1, 0), (0, 1))
        + np.roll(Z, (-1, 0), (0, 1))
        + np.roll(Z, (0, 1), (0, 1))
        + np.roll(Z, (0, -1), (0, 1))
    )


# Initialize U and V with random noise
U = np.ones((width, height)) + 0.02 * np.random.random((width, height))
V = np.zeros((width, height))

# Seed initial pattern
r = 20
U[width // 2 - r:width // 2 + r, height // 2 - r:height // 2 + r] = 0.50
V[width // 2 - r:width // 2 + r, height // 2 - r:height // 2 + r] = 0.25

# Prepare the plot
im = ax.matshow(U, origin="lower", cmap='viridis')

def update():
    global U, V

    # Compute the Laplacians and update U and V
    Lu = laplacian(U)
    Lv = laplacian(V)

    uvv = U * V * V
    U += (Du * Lu - uvv + F * (1 - U)) * dt
    V += (Dv * Lv + uvv - (F + k) * V) * dt

    # Clip values to maintain numerical stability
    np.clip(U, 0, 1, out=U)
    np.clip(V, 0, 1, out=V)

    # Update the plot
    ax.matshow(U, origin="lower", cmap='viridis')
    camera.snap()

for _ in range(100):
    update()

# Create an animation
ani = camera.animate()
plt.show()
