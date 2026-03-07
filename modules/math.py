import sys
import os
import random
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
import main
first = random.randint(1,100)
second = random.randint(1,100)

def start():
    calculation = random.choice(["plus","minus","multiplication","division"])
    if calculation == "plus":
        answer = first + second
        return answer
    elif calculation == "minus":
        answer = first - second
        return answer
    elif calculation == "multiplication":
        answer = first * second
        return answer
    elif calculation == "division":
        answer = first / second
        return answer