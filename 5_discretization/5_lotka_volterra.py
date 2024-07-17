import matplotlib.pyplot as plt
import numpy as np
from scipy.integrate import solve_ivp

def f(t, y, k):
    a, c = y
    return (
        a*(k[0, 0] + k[0, 1]*c),
        c*(k[1, 0] + k[1, 1]*a)
    )

y0 = [30, 10]   # 30 травоядных, 10 хищников
k = np.array([
    (2, -1),
    (-6, 1)
])
t_span = 0, 20
sol = solve_ivp(f, t_span, y0, args=(k,), method="RK23")
t, (a, c) = sol.t, sol.y

fig, ax = plt.subplots()

ax.plot(t, a, label="Травоядные $a(t)$")
ax.plot(t, c, label="Хищники $c(t)$")
ax.set(xlabel="Время", ylabel="Численность")
ax.legend()
ax.grid(ls=":")

fig.savefig(f"{__file__.split('.')[0]}.png", dpi=300)
# plt.show()
