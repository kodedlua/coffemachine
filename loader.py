import json

class Loader(object):
    def __init__(self):
        self.created = True

    def load(self):
        template = []
        with open("templates/template.txt") as template_file:
            for line in template_file.readlines():
                template.append(f"{line.strip()}")
                # print(line)
        config = []
        with open("templates/template.json") as template_config:
            config = json.load(template_config)
                # print(line)
        return template, config