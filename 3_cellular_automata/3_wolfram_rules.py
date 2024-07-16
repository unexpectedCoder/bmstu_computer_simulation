import matplotlib.pyplot as plt
import numpy as np
from celluloid import Camera

RULES = {
    30: {
        (1, 1, 1): 0,
        (1, 1, 0): 0,
        (1, 0, 1): 0,
        (1, 0, 0): 1,
        (0, 1, 1): 1,
        (0, 1, 0): 1,
        (0, 0, 1): 1,
        (0, 0, 0): 0
    },
    32: {
        (1, 1, 1): 0,
        (1, 1, 0): 0,
        (1, 0, 1): 1,
        (1, 0, 0): 0,
        (0, 1, 1): 0,
        (0, 1, 0): 0,
        (0, 0, 1): 0,
        (0, 0, 0): 0
    },
    90: {
        (1, 1, 1): 0,
        (1, 1, 0): 1,
        (1, 0, 1): 0,
        (1, 0, 0): 1,
        (0, 1, 1): 1,
        (0, 1, 0): 0,
        (0, 0, 1): 1,
        (0, 0, 0): 0
    },
    108: {
        (1, 1, 1): 0,
        (1, 1, 0): 1,
        (1, 0, 1): 1,
        (1, 0, 0): 0,
        (0, 1, 1): 1,
        (0, 1, 0): 1,
        (0, 0, 1): 0,
        (0, 0, 0): 0
    },
    110: {
        (1, 1, 1): 0,
        (1, 1, 0): 1,
        (1, 0, 1): 1,
        (1, 0, 0): 0,
        (0, 1, 1): 1,
        (0, 1, 0): 1,
        (0, 0, 1): 1,
        (0, 0, 0): 0
    },
    160: {
        (1, 1, 1): 1,
        (1, 1, 0): 0,
        (1, 0, 1): 1,
        (1, 0, 0): 0,
        (0, 1, 1): 0,
        (0, 1, 0): 0,
        (0, 0, 1): 0,
        (0, 0, 0): 0
    }
}

def run_wolfram(ca, rule: int, until: int):
    fig, ax = plt.subplots()
    camera = Camera(fig)

    ax.matshow(ca, cmap="binary")
    camera.snap()

    rule = RULES[rule]
    for i in range(until):
        prev = ca[i]
        new = prev.copy()
        for j in range(1, len(prev) - 1):
            index = prev[j-1], prev[j], prev[j+1]
            new[j] = rule[index]
        ca.append(new)

        ax.matshow(ca, cmap="binary")
        camera.snap()
    
    return (fig, ax), camera.animate()

rg = np.random.default_rng()

until = 201
ca = [[0 for _ in range(until + 2)]]
ca[0][-2] = 1
# ca = [rg.integers(0, 2, 2*until + 2)]
# ca[0][0], ca[0][-1] = 0, 0

rule = 110
(fig, ax), ani = run_wolfram(ca, rule, until)

ax.set_xticks([])
ax.set_yticks([])
ani.save(
    f"{__file__.split('.')[0]}_rule_{rule}.gif",
    dpi=200
)
