from lorem_text import lorem
import json


def get_messages(value_on_submit):
    answers = get_answers(value_on_submit)
    return [
        {
            "direction": "received",
            "avatar": "bot.png",
            "content": lorem.sentence()
        },
        {
            "direction": "outgoing",
            "avatar": "user.png",
            "content": lorem.sentence()
        },
        {
            "direction": "received",
            "avatar": "bot.png",
            "content":lorem.sentence()
        }
    ]


def read_rules_from_json():
    with open('config.json', encoding='utf-8') as config_file:
        config_data = json.load(config_file)
    return config_data


def get_answers(value_on_submit):
    rules = read_rules_from_json()
    start_msg = value_on_submit + rules['hard-rule']
    print(start_msg)
    print(rules)
