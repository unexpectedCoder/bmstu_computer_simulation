from random import randint

attempts = 10_000
success = len(
    [
        _
        for _ in range(attempts)
        if randint(0, 1) + randint(0, 1) + randint(0, 1) + randint(0, 1) == 3
    ]
)

print("Попыток:", attempts)
print("Событий:", success)
print("Частота:", success / attempts)
