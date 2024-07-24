import random as rand

def runSim(goal, num_trials):
    total = 0
    for _ in range(num_trials):
        result = ""
        for _ in range(len(goal)):
            result += str(roll_die())
        if result == goal:
            total += 1
    
    print("Реальная вероятность:\t", round(1/(6**len(goal)), 8))
    est_prob = round(total/num_trials, 8)
    print("Оценка вероятности:\t", round(est_prob, 8))

def roll_die():
    """returns a random int between 1 and 6"""
    return rand.choice([1, 2, 3, 4, 5, 6])

runSim('11111', 1000)
