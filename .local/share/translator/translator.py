#!/home/magax/.local/share/translator/venv/bin/python
from googletrans import Translator
import sys
import json
from difflib import get_close_matches
from os import path

basepath = path.dirname(__file__)
filepath = path.abspath(path.join(basepath, 'data.json'))
data = json.load(open(filepath))
translator = Translator()

if len(sys.argv) > 2:
    src = sys.argv[1]
    dst = sys.argv[2]
else:
    src = 'en'
    dst = 'ru'


def meaning(w):
    w = w.lower()
    if w in data:
        return data[w]
    elif w.title() in data:
        return data[w.title()]
    elif w.upper() in data:
        return data[w.upper()]
    elif len(get_close_matches(w, data.keys())) > 0:
        yn = input("Did you mean %s instead? Enter Y if yes, or N if no: " % get_close_matches(w, data.keys())[0])
        if yn == "Y":
            return data[get_close_matches(w, data.keys())[0]]
        elif yn == "N":
            return "The word doesn't exist. Please double check it."
        else:
            return "We didn't understand your entry."
    else:
        return "The word doesn't exist. Please double check it."


def multi_input():
    try:
        while True:
            data=input()
            if not data: break
            yield data + ' '
    except KeyboardInterrupt:
        return


print('Введите слово или вставьте свой текст: ')

lines = list(multi_input())

if len(lines) == 0:
    print('Отмена')
    sys.exit()
elif len(''.join(lines).split()) == 1 and len(sys.argv) == 1:
    text = meaning(''.join(lines).strip())
    if type(text) == list:
        for item in text:
            print(item)
            text = ''.join(text)
    else:
        print(text)
        text = ''.join(text)
else:
    raw_text = ''.join(lines)
    text = raw_text.replace('\n', ' ').replace('. ', '. \n').replace('- ', '').replace(' .', '.')
    
result = translator.translate(text, src=src, dest=dst)
print(result.text)

# ja - японский
# fr - французский
# la - латинский
# de - немецкий
# it - итальянский
# pl - польский
