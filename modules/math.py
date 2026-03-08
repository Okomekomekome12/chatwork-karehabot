import sys
import os
import random
import time
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
import main

def start(cw):
    first = random.randint(1,100)
    second = random.randint(1,100)
    calculation = random.choice(["plus","minus","multiplication","division"])
    if calculation == "plus":
        cw.messagesend(f"{first} + {second} = ? \n10秒以内で答えてください")
        answer = first + second
        time.sleep(10)
        messages = cw.get_new_messages()["body"]
        print(messages)
        if int(messages) == answer:
            cw.messagesend("正解です")
        else:
            cw.messagesend("不正解です")
        return answer
    elif calculation == "minus":
        cw.messagesend(f"{first} - {second} = ?\n10秒以内に答えてください")
        answer = first - second
        time.sleep(10)
        messages = cw.get_new_messages()["body"]
        print(messages)
        if int(messages) == answer:
            cw.messagesend("正解です")
        else:
            cw.messagesend("不正解です")
        return answer
    elif calculation == "multiplication":
        cw.messagesend(f"{first} × {second} = ?\n15秒以内に答えてください")
        answer = first * second
        time.sleep(15)
        messages = cw.get_new_messages()["body"]
        print(messages)
        if int(messages) == answer:
            cw.messagesend("正解です")
        else:
            cw.messagesend("不正解です")
        return answer
    elif calculation == "division":
        cw.messagesend(f"{first} ÷ {second} = ?\n15秒以内に答えてください")
        answer = first / second
        time.sleep(15)
        messages = cw.get_new_messages()["body"]
        print(messages)
        if float(messages) == answer:
            cw.messagesend("正解です")
        else:
            cw.messagesend("不正解です")
        return answer