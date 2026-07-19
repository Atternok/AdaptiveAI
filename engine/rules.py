import json
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RULES_FILE = os.path.join(BASE_DIR, "data", "rules.json")

with open(RULES_FILE, "r") as f:
    RULES = json.load(f)


def check_rule(user_input):
    text = user_input.lower().strip()

    if text in RULES:
        return True, RULES[text]

    return False, None