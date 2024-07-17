import matplotlib.pyplot as plt
import numpy as np
from scipy.integrate import solve_ivp

def f(t, y, eps):
    s = y[0]
    return -s / eps

eps1, eps2 = 0.1, 0.01
t = np.linspace(0, 1, 100)
s1 = np.exp(-t / eps1)
s2 = np.exp(-t / eps2)

s0 = [1]
t_span = 0, 1
sol = solve_ivp(f, t_span, s0, args=(eps2,), method="LSODA")
t3, s3 = sol.t, sol.y[0]

fig, ax = plt.subplots()

ax.plot(t, s1, label=r"Точное $\varepsilon=0.10$")
ax.plot(t, s2, label=r"Точное $\varepsilon=0.01$")
ax.plot(t3, s3, c="k", marker=".", ls="", label="Численное решение")
ax.set(xlabel="$t$", ylabel="$s$")
ax.grid(ls=":")
ax.legend()

fig.savefig(f"{__file__.split('.')[0]}.png", dpi=300)
# plt.show()
