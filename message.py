from lorem_text import lorem
import json
from openai import OpenAI
import os


def get_messages(value_on_submit):
    return get_answers(value_on_submit)


def read_rules_from_json():
    with open('config.json', encoding='utf-8') as config_file:
        config_data = json.load(config_file)
    return config_data


def get_answers(value_on_submit):
    rules = read_rules_from_json()
    value_on_submit = value_on_submit + "." if not str(value_on_submit).endswith(".") else value_on_submit
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    messages = [{"role": "system", "content": "You are a helpful assistant."}]

    return get_chatgpt_responses(value_on_submit, client, messages, rules)


def get_chatgpt_responses(value_on_submit, client, messages, rules):
    # Start message from UI
    message = value_on_submit
    all_chat_messages = [{"direction": "outgoing", "avatar": "user.png", "content": message}]
    message = value_on_submit + rules['hard-rule']

    # First answer and first generated code
    messages, all_chat_messages, source_code_str = get_first_generated_code(message, messages, client, all_chat_messages)

    while len(rules['rules']) > 0:
        # Rule - pass or not?
        current_rule = rules['rules'].pop(0)
        all_chat_messages, chat_message, messages = send_the_question(current_rule, source_code_str, messages, client, all_chat_messages)

        # Good generated code
        if str(chat_message).startswith("Igen"):
            all_chat_messages.append({"direction": "received", "avatar": "bot.png", "content": chat_message})
        elif str(chat_message).startswith("Nem"):
            # Not good -> regenerate based on rule
            all_chat_messages.append({"direction": "received", "avatar": "bot.png", "content": chat_message})
            source_code_str, messages, all_chat_messages = code_regenerate_based_on_rule(current_rule, messages, client,
                                                                                         all_chat_messages, rules, source_code_str)

    return all_chat_messages


def get_first_generated_code(message, messages, client, all_chat_messages):
    messages.append({"role": "user", "content": message})
    response = client.chat.completions.create(model="gpt-4o", messages=messages)
    chat_message = response.choices[0].message.content
    source_code_str = chat_message.split('```python')[1].split('```')[0]
    all_chat_messages.append({"direction": "received", "avatar": "bot.png", "content": source_code_str})
    messages.append({"role": "assistant", "content": chat_message})
    return messages, all_chat_messages, source_code_str


def send_the_question(current_rule, source_code_str, messages, client, all_chat_messages):
    message = current_rule + ', igen vagy nem? ' + str(source_code_str)
    all_chat_messages.append({"direction": "outgoing", "avatar": "user.png", "content": current_rule + ', igen vagy nem?'})
    messages.append({"role": "user", "content": message})
    response = client.chat.completions.create(model="gpt-4o", messages=messages)
    chat_message = response.choices[0].message.content
    return all_chat_messages, chat_message, messages


def code_regenerate_based_on_rule(current_rule, messages, client, all_chat_messages, rules, source_code_str):
    message, all_chat_messages = rule_conversion(current_rule, messages, client, all_chat_messages)
    source_code_str, messages, all_chat_messages = code_generation(message, messages, rules, source_code_str, client, all_chat_messages)
    return source_code_str, messages, all_chat_messages


def rule_conversion(current_rule, messages, client, all_chat_messages):
    _tmp_message = "Alakítsd át felszólító móddá az alábbi mondatot: " + current_rule
    messages.append({"role": "user", "content": _tmp_message})
    _tmp_response = client.chat.completions.create(model="gpt-4o", messages=messages)
    _tmp_chat_message = _tmp_response.choices[0].message.content

    message = 'Módosítsd az alábbi kódot, úgy hogy ' + _tmp_chat_message
    all_chat_messages.append({"direction": "outgoing", "avatar": "user.png", "content": message.capitalize()})
    return message, all_chat_messages


def code_generation(message, messages, rules, source_code_str, client, all_chat_messages):
    message += '. ' + rules['hard-rule'] + '.\n' + source_code_str
    messages.append({"role": "user", "content": message})
    response = client.chat.completions.create(model="gpt-4o", messages=messages)
    chat_message = response.choices[0].message.content
    source_code_str = chat_message.split('```python')[1].split('```')[0]
    all_chat_messages.append({"direction": "received", "avatar": "bot.png", "content": source_code_str})
    messages.append({"role": "assistant", "content": chat_message})
    return source_code_str, messages, all_chat_messages
