from pygments.formatters import HtmlFormatter
import markdown
import os
import pathlib
import re
import time
# from personalwebsite import app

"""
This class will take in Markdown and correctly render it into HTML.

Output generated can be then piped into Jinja2 style syntax with the following line:

{{ GeneratedOutput|safe }}

Please refer to this Stackoverflow post for more details:

https://stackoverflow.com/questions/3206344/passing-html-to-template-using-flask-jinja2

Written by Jared Dyreson CSUF 2021
"""

class Markdown():
    def __init__(self, path: pathlib.Path):
        if not(isinstance(path, pathlib.Path)):
            raise ValueError
        self.path = path
        self.read_contents()
        self.replaced = self.find_replace_links()
        self.format_contents()
        self.title_ = self.get_title()
        self.category = self.get_category()
        self.subcategory  = self.get_subcategory()
        self.creation_date = self.get_last_modified()

    def get_category(self):
        return os.path.basename(self.path.parent)

    def get_subcategory(self):
        return os.path.basename(os.path.dirname(os.path.dirname(self.path)))

    def find_replace_links(self):
        new_contents = []
        link_regex = re.compile("\!\[(?P<name>.*)\]\((?P<link>.*)\)")
        for line in self.contents:
            match = link_regex.match(line)
            if(match):
                flask_relative_link = f'/static/assets/{self.get_subcategory()}/{self.get_category()}/{os.path.basename(match.group("link"))}'
                # flask_relative_link = "/static/assets/arch_logo.png"
                substitute = r"![\g<name>]({})".format(flask_relative_link)
                line  = link_regex.sub(substitute, line)
            new_contents.append(line)

        self.contents = new_contents

    def format_contents(self):
        markdown_extensions = [
            'markdown.extensions.attr_list',
            'markdown.extensions.tables',
            'markdown.extensions.fenced_code',
            'codehilite'
        ]

        markdown_template = markdown.markdown(
            "\n".join(self.contents),
            output_format = 'html5',
            tab_length = 4,
            extensions = markdown_extensions
        )

        formatter = HtmlFormatter(style="friendly", full=True, cssclass="codehilite")
        markdown_css = f'<style>{formatter.get_style_defs()}</style>'
        self.formatted_contents = f'{markdown_template}{markdown_css}'

    def read_contents(self):
        self.contents = [line for line in self.path.open()]

    def size(self) -> int:
        return len(self.contents)

    def get_title(self):
        _title_re = re.compile("^#\s+(?P<title>.*)")
        try:
            match = _title_re.match(self.contents[0])
        except IndexError:
            return None
        return match.group("title") if match else None
    
    def get_last_modified(self) -> str:
        return ' '.join(time.ctime(os.path.getmtime(self.path.absolute())).split())

    def write_formatted(self):
        with open(f'{self.path.stem}.html', "w") as fp:
            fp.write(self.formatted_contents)

