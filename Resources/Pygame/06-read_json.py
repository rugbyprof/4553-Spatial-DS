import json


with open('../colors.json', 'r') as content_file:
    content = content_file.read()

content = json.loads(content)

for color in content:
    print color


