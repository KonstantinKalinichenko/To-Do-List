import os
import json


def print_with_indent(value, indent=0):
    indentation = "\t" * indent
    print(f"{indentation}{value}")


class Entry:
    def __init__(self, title, entries=None, parent=None):
        if entries is None:
            entries = []
        self.title = title
        self.entries = entries
        self.parent = parent

    def __str__(self):
        return self.title

    @classmethod
    def from_json(cls, value):
        new_entry = cls(value["title"])
        for item in value.get('entries', []):
            new_entry.add_entry(cls.from_json(item))
        return new_entry

    @classmethod
    def load(cls, filename):
        with open(filename, 'r', encoding='utf-8') as f:
            c = json.load(f)
        return cls.from_json(c)

    def add_entry(self, entry):
        self.entries.append(entry)
        entry.parent = self

    def print_entries(self, indent=0):
        print_with_indent(self, indent)
        for entry in self.entries:
            entry.print_entries(indent=indent + 1)

    def json(self):
        res = {
            'title': self.title,
            "entries": [entry.json() for entry in self.entries]
        }
        return res

    def save(self, path):
        with open(os.path.join(path, f'{self.title}.json'), 'w', encoding='utf-8') as f:
            json.dump(self.json(), f, ensure_ascii=False)