import json
import random

import questionary


def load_questions():
    new_data = {}
    with open("db/5-選擇題庫全1140224.json", "r", encoding="utf-8") as f:
        new_data["選擇題"] = json.load(f)
    with open("db/6-是非題庫全1140224.json", "r", encoding="utf-8") as f:
        new_data["是非題"] = json.load(f)
    return new_data


def change_format(questions):
    new_questions = []
    for q_type in questions:
        for q_topic in questions[q_type]:
            new_questions.extend(questions[q_type][q_topic])
    return new_questions


def load_users():
    with open("db/users.json", "r", encoding="utf-8") as f:
        users = json.load(f)
    return users


def dump_users(users):
    with open("db/users.json", "w", encoding="utf-8") as f:
        json.dump(users, f, ensure_ascii=False, indent=2)


def pick_questions(question_db, num=10):
    random.shuffle(question_db)
    questions = [question_db.pop() for _ in num]
    return questions
    

def main():
    users = load_users()
    questions = load_questions()
    questions = change_format(questions)
    
    user = questionary.text("輸入你的名稱").ask()
    if user not in users:
        users[user] = questions
    else:
        print(f"歡迎回來 {user}, 你已經練習了 {len(questions) - len(users[user])} / {len(questions)} !!!")
    questions = users[user]

    mode = questionary.select("選擇模式", choices=["練習模式", "考試模式"]).ask()
    if mode == "練習模式":
        finish = False
        while questionary.confirm("繼續?").ask():
            random.shuffle(questions)
            question = questions.pop()
            user_answer = questionary.select(message=question["題目"], choices=question["選項"],).ask()
            true_answer = question["答案"]
            if true_answer == "O":
                true_answer = 0
            if true_answer == "X":
                true_answer = 1
            true_answer = question["選項"][int(true_answer) - 1]
            
            if user_answer != true_answer:
                questions.append(question)
            print(f"{user_answer == true_answer} 答案是 {true_answer}")
        users[user] = questions
        dump_users(users)
        print("進度已記錄 bye ...")

    if mode == "考試模式":
        distribution = {
            "政府採購全生命週期概論": 2,
            "政府採購法之總則、招標及決標": 14,
            "政府採購法之履約管理及驗收": 2,
            "政府採購法之罰則及附則": 5,
            "工程及技術服務採購作業": 6,
            "財物及勞務採購作業": 6,
            "最有利標及評選優勝廠商": 6,
            "電子採購實務": 6,
            "錯誤採購態樣": 2,
            "投標須知及招標文件製作": 4,
            "採購契約": 4,
            "底價及價格分析": 3,
            "政府採購法之爭議處理": 4,
            "道德規範及違法處置": 2,
        }
        questions = load_questions()
        
        exam_questions = []
        for topic in distribution:
            exam_questions.extend(random.sample(questions["是非題"][topic], distribution[topic] * 1))
            exam_questions.extend(random.sample(questions["選擇題"][topic], distribution[topic] * 2))

        index = 1
        while exam_questions:
            random.shuffle(exam_questions)
            question = exam_questions.pop()
            user_answer = questionary.select(message=f"第 {index} 題: {question['題目']}", choices=question["選項"],).ask()
            true_answer = question["答案"]
            if true_answer == "O":
                true_answer = 0
            if true_answer == "X":
                true_answer = 1
            true_answer = question["選項"][int(true_answer) - 1]
            print(f"{user_answer == true_answer} 答案是 {true_answer}")
            index += 1
        print("結束了 ...")


if __name__ == "__main__":
    main()