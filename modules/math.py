import sys
import os
import random
import time
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
import main

def start(cw):
    plusminusfirst = random.randint(1,100)
    plusminussecond = random.randint(1,100)
    kakezanfirst = random.randint(1,50)
    kakezansecond = random.randint(1,50)
    warizanfirst = random.randint(20,30)
    warizansecond = random.randint(1,19)
    calculation = random.choice(["plus","minus","multiplication","division"])
    if calculation == "plus":
        cw.messagesend(f"{plusminusfirst} + {plusminussecond} = ? \n10秒以内で答えてください")
        answer = plusminusfirst + plusminussecond
        time.sleep(10)
        messages = cw.get_new_messages()["body"]
        print(messages)
        if int(messages) == answer:
            cw.messagesend("正解です")
        else:
            cw.messagesend("不正解です")
        return answer
    elif calculation == "minus":
        cw.messagesend(f"{plusminusfirst} - {plusminussecond} = ?\n10秒以内に答えてください")
        answer = plusminusfirst - plusminussecond
        time.sleep(10)
        messages = cw.get_new_messages()["body"]
        print(messages)
        if int(messages) == answer:
            cw.messagesend("正解です")
        else:
            cw.messagesend("不正解です")
        return answer
    elif calculation == "multiplication":
        cw.messagesend(f"{kakezanfirst} × {kakezansecond} = ?\n15秒以内に答えてください")
        answer = kakezanfirst * kakezansecond
        time.sleep(15)
        messages = cw.get_new_messages()["body"]
        print(messages)
        if int(messages) == answer:
            cw.messagesend("正解です")
        else:
            cw.messagesend("不正解です")
        return answer
    elif calculation == "division":
        cw.messagesend(f"{warizanfirst} ÷ {warizansecond} = ?\n15秒以内に答えてください")
        answer = warizanfirst / warizansecond
        time.sleep(15)
        messages = cw.get_new_messages()["body"]
        print(messages)
        if float(messages) == answer:
            cw.messagesend("正解です")
        else:
            cw.messagesend("不正解です")
        return answer