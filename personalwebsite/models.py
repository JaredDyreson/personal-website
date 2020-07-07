from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from personalwebsite.MarkdownParser import Markdown
import pathlib


class BlogItem():
    def __init__(self, source: Markdown):
        if not(isinstance(source, Markdown)):
            raise ValueError

        self.category = source.category
        self.contents = source.formatted_contents
        self.creation_date = source.creation_date
        self.source = source
        self.title = source.title_

class BlogCategory():
    def __init__(self, category: str, 
                    image_src: str, description: str):
        if not(isinstance(category, str) and
               isinstance(image_src, str) and
               isinstance(description, str)):
               raise ValueError
        self.category = category
        self.description = description
        self.image_path = image_src

class PortfolioItem():
    def __init__(self, title, content, number,
                    image_path, demo_link, doc_link, src_link):
        if not(isinstance(title, str) or
                isinstance(content, str) or
                isinstance(number, int) or
                isinstance(image_path, str) or
                isinstance(demo_link, str) or
                isinstance(doc_link, str) or
                isinstance(src_link, str)):
            raise ValueError

        self.content = content
        self.demo_link = demo_link
        self.doc_link = doc_link
        self.image_path = image_path
        self.number = number
        self.src_link = src_link
        self.title_ = title


class GasolineCalculatorForm(FlaskForm):

    current_price = StringField(
        'Current Gasoline Price',
        validators=[DataRequired()]
    )

    current_miles_left = StringField(
        'Miles to Empty',
        validators=[DataRequired()]
    )

    submit = SubmitField('Calculate')
