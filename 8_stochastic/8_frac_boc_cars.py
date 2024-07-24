import random as rand

def frac_box_cars(num_tests):
    num_box_cars = 0
    for i in range(num_tests):
        if roll_die() == 6 and roll_die() == 6:
            num_box_cars += 1
    return num_box_cars / num_tests

def roll_die():
    """returns a random int between 1 and 6"""
    return rand.choice([1, 2, 3, 4, 5, 6])

print(f"Частота двух 6: {frac_box_cars(100000)*100}%")
