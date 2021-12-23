import codecs
import json


def get_type(sym):
    if sym in ['+', '-'] and q['type'] == '':
        return 'single'
    elif sym in ['+', '-']:
        return 'many'
    elif sym in ['R', 'L']:
        return 'compliance'
    else:
        return 'unknown'


def is_int(s):
    try:
        int(s)
        return True
    except ValueError:
        return False


questions = []
q = None
f = open("questions/ekologia.txt", encoding='utf-8')
for line in f.readlines():
    line = line.replace('\r', '').replace('\n', '').strip()
    if not len(line):
        continue

    if line[0] in ['I', 'Q', 'S'] and len(q['vars']) != 0 or q is None:
        questions.append(q)
        q = {'type': "", 'theme': "", 'task': "", 'question': "", 'vars': []}

    if line[0] == 'I':
        q['theme'] = line.split('}')[-1][1:].strip()
    elif line[0] == 'Q':
        q['task'] = line[2:].strip()
    elif line[0] == 'S':
        q['question'] = line[2:].strip()
    elif line[0] in ['+', '-', 'R', 'L'] or is_int(line[0]):
        q['vars'].append(line)
        q['type'] = get_type(line[0])

del q
del questions[0]
f.close()

for q in questions:
    if q is None or q['type'] == "compliance":
        continue
    bad_answers = 0
    for var in q['vars']:
        if var[0] == '-':
            bad_answers += 1
    if bad_answers == 0:
        q['type'] = "enter"
    elif len(q['vars']) - bad_answers > 1:
        q['type'] = "many"
    else:
        q['type'] = "single"

with codecs.open("../docs/scripts/questions.js", "w", "utf-8") as file:
    file.write(u'\ufeff')
    file.write("questions = ")
    file.writelines(json.dumps(questions, ensure_ascii=False))

print(len(questions))
