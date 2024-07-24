import matplotlib.pyplot as plt
import numpy as np
import random as rand
from tqdm import trange

def random_walk(steps: int):
    x, y = 0, 0
    drunk = [(x, y)]
    directions = "n", "w", "s", "e"

    for _ in range(steps):
        d = rand.choice(directions)
        match d:
            case "n":
                y += 1
            case "s":
                y -= 1
            case "w":
                x -= 1
            case "e":
                x += 1
            case _:
                raise RuntimeError
        drunk.append((x, y))
    
    return np.array(drunk)

drunks = [random_walk(1000) for _ in trange(1000)]

fig, ax = plt.subplots()

for drunk in drunks:
    ax.plot(drunk[-1, 0], drunk[-1, 1], c="b", marker=".", ls="")
ax.plot([0], [0], marker="^", ls="", c="magenta")
ax.set(xlabel="$x$", ylabel="$y$", aspect="equal")

fig.savefig(f"{__file__.split('.')[0]}.png", dpi=300)
# plt.show()
