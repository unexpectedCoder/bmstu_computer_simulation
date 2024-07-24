import random as rand

def roll_die():
    """returns a random int between 1 and 6"""
    return rand.choice([1, 2, 3, 4, 5, 6])

def testRoll(n = 10):
    result = ""
    for _ in range(n):
        result = result + str(roll_die())
    print(result)
