import json
from pprint import pprint


def get_motivational_phrases():
    with open('utils/motivational_phrases/motivational_phrases.json') as f:
        data = json.loads(f.read())
        return data


def get_motivational_phrase_by_marathon_day(marathon_day):
    phrases = get_motivational_phrases()
    return phrases.get(str(marathon_day))







