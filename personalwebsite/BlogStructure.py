import pathlib
import os
import pprint
import re
from termcolor import colored

class BlogHierarchy():
    def __init__(self, path: pathlib.Path):
        if not(isinstance(path, pathlib.Path)):
            raise ValueError

        self.base = path.absolute()
        self.relative = path
        self.structure = self.generate_structure()
        self.topics = self.get_topics()

    def generate_structure(self):
        structure = {'': {}}
        for dirpath, dirnames, filenames in os.walk(self.base.name):
            state = structure
            dirpath = dirpath[len(self.base.name):]
            for subdir in dirpath.split(os.sep):
                based = state
                state = state[subdir]
            if(dirnames):
                for dn in dirnames:
                    state[dn] = {}
            else:
                based[subdir] = filenames
        return structure
    
    def get_topics(self):
        return list(self.get_topic_structure().keys()) if self.structure is not None else []

    def get_topic_structure(self):
        return self.structure['']

    def get_subtopic_structure(self):
        s = {}
        for topic in self.topics:
            s[topic] = self.get_topic_structure()[topic]
        return s

    def search(self, path: tuple):
        if not(isinstance(path, tuple)):
            raise ValueError

        root, subject, filename = path

        if not(isinstance(root, str) and
               isinstance(subject, str) and
               isinstance(filename, str)):
               raise ValueError

        path_to_file = pathlib.Path(os.path.join(self.base, root, subject, filename))

        if not(path_to_file.exists()):
                 raise FileNotFoundError

        return path_to_file

    def grep_blog_contents(self, path: pathlib.Path, regex: str):
        if not(isinstance(path, pathlib.Path) and
               isinstance(regex, str)):
            raise ValueError

        contents = [line for line in path.open()]
        reg = re.compile(regex)
        relative_path = '/'.join(path.parts[len(self.base.parts):]) 
        for x, line in enumerate(contents):
            match = reg.search(line)
            if(match):
                start, end = match.span()
                match_format = colored(line[start:end], 'red')
                index_format = colored(f'{relative_path}:{x}', 'green')
                print(f'{index_format} {match_format}{line[end:]}')
