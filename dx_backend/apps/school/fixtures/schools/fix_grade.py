import json

with open('FireArtsSchool.json', 'r') as file:
    data = json.load(file)

    for skill in data['skills']:
        skill['grade'] += 1
        print(skill['grade'])

with open('FireArtsSchool.json', 'w') as file:
    json.dump(data, file, indent=2)