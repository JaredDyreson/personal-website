import pathlib
import re

class Markdown():
    def __init__(self, path: pathlib.Path):
        if not(isinstance(path, pathlib.Path)):
            raise ValueError
        self.path = path
        self.read_contents()

    def read_contents(self):
        self.contents = [line for line in self.path.open()]

    def size(self) -> int:
        return len(self.contents)

    def title(self):
        _title_re = re.compile("^#\s+(?P<title>.*)")
        match = _title_re.match(self.contents[0])
        return match.group("title") if match else None
