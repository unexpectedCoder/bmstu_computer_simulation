import matplotlib.pyplot as plt
import numpy as np
import random as rand
from abc import ABC, abstractmethod
from tqdm import trange


class Location:
    def __init__(self, x: float, y: float):
        self._x = x
        self._y = y

    def __str__(self):
        return f"<{self._x}, {self._y}>"

    def move(self, dx: float, dy: float):
        return Location(self._x + dx, self._y + dy)

    def dist_from(self, other: "Location"):
        x_dist = self._x - other._x
        y_dist = self._y - other._y
        return (x_dist**2 + y_dist**2)**0.5
    
    @property
    def xy(self):
        return self._x, self._y


class Drunk(ABC):
    @abstractmethod
    def take_step(self):
        pass
    

class UsualDrunk(Drunk):
    STEPS = [(0, 1), (0, -1), (1, 0), (-1, 0)]

    def take_step(self):
        return rand.choice(self.STEPS)


class ColdDrunk(Drunk):
    STEPS = [(0, 0.9), (0, -1.1), (1, 0), (-1, 0)]

    def take_step(self):
        return rand.choice(self.STEPS)


class Field:
    def __init__(self):
        self.drunks_loc = {}
    
    def add_drunk(self, drunk: Drunk, loc: Location):
        if drunk in self.drunks_loc:
            raise ValueError("Этот выпивоха уже на учёте")
        self.drunks_loc[drunk] = loc
    
    def move_drunk(self, drunk):
        if drunk not in self.drunks_loc:
            raise ValueError("Не... не знаем такого... *ик*")
        x_dist, y_dist = drunk.take_step()
        current_location = self.drunks_loc[drunk]
        self.drunks_loc[drunk] = current_location.move(x_dist, y_dist)

    def get_loc(self, drunk: Drunk):
        if drunk not in self.drunks_loc:
            raise ValueError("Не... не знаем такого... *ик*")
        return self.drunks_loc[drunk]


def sim_walks(d_class: type[Drunk], n_steps: int, n_trials: int):
    drunk = d_class()
    origin = Location(0, 0)
    xy, distances = [], []

    for _ in trange(n_trials):
        f = Field()
        f.add_drunk(drunk, origin)
        distances.append(walk(f, drunk, n_steps))
        xy.append(f.get_loc(drunk).xy)
    
    return np.array(xy), distances


def walk(f: Field, d: Drunk, n_steps: int):
    start = f.get_loc(d)
    for _ in range(n_steps):
        f.move_drunk(d)
    return start.dist_from(f.get_loc(d))


steps = np.arange(1000, 10_001, 1000)
n_trials = 1000

mean_dist_usual, mean_dist_cold = [], []
xy_usual, xy_cold = [], []
for n_steps in steps:
    xy_u, dist_usual = sim_walks(UsualDrunk, n_steps, n_trials)
    xy_c, dist_cold = sim_walks(ColdDrunk, n_steps, n_trials)
    mean_dist_usual.append(np.mean(dist_usual))
    mean_dist_cold.append(np.mean(dist_cold))
    xy_usual.append(xy_u)
    xy_cold.append(xy_c)

fig, ax = plt.subplots(num="means")

ax.plot(steps, mean_dist_usual, label="UsualDrunk")
ax.plot(steps, mean_dist_cold, label="ColdDrunk")
ax.set(
    xlabel="Число шагов (steps)",
    ylabel="Расстояние от бара",
    title="Среднее расстояние от бара (1000 испытаний)"
)
ax.legend()
fig.savefig(f"{__file__.split('.')[0]}_means.png", dpi=300)

xy_u, dist_usual = sim_walks(UsualDrunk, 10_000, 1_000)
xy_c, dist_cold = sim_walks(ColdDrunk, 10_000, 1_000)

fig, ax = plt.subplots(num="xy")

ax.plot(
    xy_u[:, 0], xy_u[:, 1], ls="", marker="+", c="k", label="UsualDrunk"
)
ax.plot(
    xy_c[:, 0], xy_c[:, 1],
    ls="", marker="^", c="r", markeredgecolor="k", label="ColdDrunk"
)
ax.set(
    xlabel="Число шагов запад/восток",
    ylabel="Число шагов север/юг",
    title="Конечные положения выпивох (10 000 шагов)",
    aspect="equal"
)
ax.legend()
fig.savefig(f"{__file__.split('.')[0]}_endpoints.png", dpi=300)

# plt.show()
