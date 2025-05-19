import json


def update_questions(data):
    with open("db/5-select-1140519.json", "r", encoding="utf-8") as f:
        new_data = json.load(f)
        for key in new_data:
            data["選擇題"][key].extend(new_data[key])
    with open("db/6-yesno-1140519.json", "r", encoding="utf-8") as f:
        new_data = json.load(f)
        for key in new_data:
            data["是非題"][key].extend(new_data[key])
    return data


def load_users():
    with open("db/users.json", "r", encoding="utf-8") as f:
        users = json.load(f)
    return users


def dump_users(users):
    with open("db/users.json", "w", encoding="utf-8") as f:
        json.dump(users, f, ensure_ascii=False, indent=2)

    
def main():
    users = load_users()

    for key in users:
        users[key] = update_questions(users[key])
    
    dump_users(users)
    

if __name__ == "__main__":
    main()