import matplotlib.pyplot as plt
import random as rand
from tqdm import tqdm

CARDS = [i for i in range(13)] * 4  # 52 карты
rand.shuffle(CARDS)                 # перемешали
S = len(CARDS)                      # размер колоды

def play(pa: list, pb: list, rounds: int):
    rounds = [i for i in range(1, rounds + 1)]
    history = [len(pa)]

    for _ in tqdm(rounds[1:]):
        if pa == [] or pb == []:
            return rounds[:len(history)], history
        
        a, b = pa.pop(0), pb.pop(0)
        if a > b:
            pa.extend([a, b])
            history.append(len(pa))
        elif a < b:
            pb.extend([a, b])
            history.append(len(pa))
        else:
            war(pa, pb, history)
    
    return rounds[:len(history)], history

def war(pa: list, pb: list, history: list):
    if pa == [] or pb == []:
        return
    
    a = pa[:4].copy()
    b = pb[:4].copy()
    del pa[:4]
    del pb[:4]
    
    if a[-1] > b[-1]:
        pa.extend(a + b)
        history.append(len(pa))
    elif a[-1] < b[-1]:
        pb.extend(a + b)
        history.append(len(pa))
    else:
        if len(pa) <= 1 or len(pb) <= 1:
            return
        a.append(pa.pop(0))
        b.append(pb.pop(0))
        if a[-1] > b[-1]:
            pa.extend(a + b)
            history.append(len(pa))
        elif a[-1] < b[-1]:
            pb.extend(a + b)
            history.append(len(pa))
        else:
            war(pa, pb)

# Распределение по двум игрокам
player_a = CARDS[:S//2]
player_b = CARDS[S//2:]

rounds, history = play(player_a, player_b, 1000)

fig, ax = plt.subplots(figsize=(15, 6))

ax.step(rounds, history, where="mid")
ax.set(xlabel="Раунд", ylabel="Число карт у Игрока 1")
ax.grid(ls=":")

# fig.savefig(f"{__file__.split('.')[0]}.png", dpi=300)
plt.show()
