import json
import os 

class colors(object):
    def __init__(self,file_name):
        with open(file_name, 'r') as content_file:
            content = content_file.read()

        self.content = json.loads(content)

    def get_rgb(self,name):
        for c in self.content:
            if c['name'] == name:
                return (c['rgb'][0],c['rgb'][1],c['rgb'][2])
        return None

class us_states(object):
    def __init__(self,file_name):
        with open(file_name, 'r') as content_file:
            content = content_file.read()

        self.content = json.loads(content)

    def get_state_polygon(self,name):
        for s in self.content:
            if s['name'] == name:
                return s['borders']
        return None


dir_path = os.path.dirname(os.path.realpath(__file__))
file_name = dir_path + '/../Json_Files/colors.json'
c = colors(file_name)a

print(c.get_rgb('pink'))

file_name = dir_path + '/../Json_Files/state_borders.json'
s = us_states(file_name)

print(s.get_state_polygon('Delaware'))