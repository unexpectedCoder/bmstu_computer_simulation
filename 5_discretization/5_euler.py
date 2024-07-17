import matplotlib.pyplot as plt
import numpy as np
from typing import Callable

def solve(f: Callable,
          x0: float,
          dt: float,
          until: float,
          *args):
    # Здесь массив x это, по сути, температура T(t_n)
    t = 0.
    t_store, x_store = [t], [x0]

    while t < until:
        x_store.append(f(x_store[-1], dt, *args))
        t += dt
        t_store.append(t)
    
    return np.array(t_store), np.array(x_store)

def right_part(T: float, dt: float, *args):
    r, T_s = args
    return T - dt*r*(T - T_s)

T0, T_s = 373, 293  # К
r = 0.08            # 1/мин
t = 25              # мин
N1, N2 = 10, 50
dt_1, dt_2 = t/(N1 - 1), t/(N2 - 1)

t1, T1 = solve(right_part, T0, dt_1, t, r, T_s)
t2, T2 = solve(right_part, T0, dt_2, t, r, T_s)

fig, ax = plt.subplots()

ax.plot(t1, T1 - 273, marker=".", label=f"$N={N1}$")
ax.plot(t2, T2 - 273, marker=".", label=f"$N={N2}$")
ax.set(xlabel="$t$, мин", ylabel="$T$, $\degree$C")
ax.legend()
ax.grid(ls=":")

fig.savefig(f"{__file__.split('.')[0]}_coffee.png", dpi=300)
plt.show()
