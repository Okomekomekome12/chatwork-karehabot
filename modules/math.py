import random

# 出題中の問題を保存する辞書（message_idをキーにする）
current_questions = {}

def start(account_id, cw):
    """計算問題を出題"""
    
    # 問題の種類をランダムに選択
    calculation = random.choice(["plus", "minus", "multiplication", "division"])
    
    if calculation == "plus":
        num1 = random.randint(1, 100)
        num2 = random.randint(1, 100)
        answer = num1 + num2
        message = f"{num1} + {num2} = ?\n答えを返信してください"
        
    elif calculation == "minus":
        num1 = random.randint(1, 100)
        num2 = random.randint(1, 100)
        answer = num1 - num2
        message = f"{num1} - {num2} = ?\n答えを返信してください"
        
    elif calculation == "multiplication":
        num1 = random.randint(1, 20)
        num2 = random.randint(1, 20)
        answer = num1 * num2
        message = f"{num1} × {num2} = ?\n答えを返信してください"
        
    elif calculation == "division":
        num1 = random.randint(20, 30)
        num2 = random.randint(1, 19)
        answer = num1 / num2
        message = f"{num1} ÷ {num2} = ?\n答えを返信してください（小数可）"
    
    cw.messagesend(message)
    
    # 問題を保存（account_idをキーに）
    current_questions[account_id] = {
        "type": calculation,
        "answer": answer
    }


def answer(account_id, body, cw):
    """回答をチェック"""
    
    question = current_questions.pop(account_id)
    calculation_type = question["type"]
    correct_answer = question["answer"]
    
    # bodyから数字部分を抽出
    # "[返信 aid=11156582 to=room_id-message_id]カレハさん\n67"
    # → "67" を取り出す
    lines = body.split('\n')
    if len(lines) > 1:
        user_answer = lines[-1].strip()  # 最後の行
    else:
        user_answer = body.strip()
    
    try:
        if calculation_type == "division":
            if float(user_answer) == correct_answer:
                cw.messagesend(f"正解です！答えは {correct_answer} です")
            else:
                cw.messagesend(f"不正解です。答えは {correct_answer} でした")
        else:
            if int(user_answer) == correct_answer:
                cw.messagesend(f"正解です！答えは {correct_answer} です")
            else:
                cw.messagesend(f"不正解です。答えは {correct_answer} でした")
    except ValueError:
        cw.messagesend(f"数字を入力してください。正解は {correct_answer} でした")