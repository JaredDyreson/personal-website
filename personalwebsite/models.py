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
        self.subcategory = source.subcategory
        self.contents = source.formatted_contents
        self.truncate_contents = source.truncated_contents
        self.creation_date = source.creation_date
        self.source = source
        self.title = source.title_
        self.file_name = source.path.name
        self.base_file_name = self.file_name.split('.')[0]

    def __repr__(self):
        return f"""
        Category: {self.category}
        Subcategory: {self.subcategory}
        Last modified: {self.creation_date}
        Title: {self.title}
        """

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
    def __init__(self, title : str, description : str,
                    image_path : str, doc_link : str,
                    src_link : str, authors: list, languages: list):
        if not(isinstance(title, str) or
                isinstance(description, str) or
                isinstance(image_path, str) or
                isinstance(doc_link, str) or
                isinstance(src_link, str) or
                isinstance(authors, list) or
                isinstance(languages, list)):
            raise ValueError

        self.authors = authors
        self.description = description
        self.doc_link = doc_link # should point to an official PDF rendition or article
        self.image_path = image_path
        self.languages = languages
        self.name = title
        self.src_link = src_link


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

class ServiceForm(FlaskForm):
    service_name = StringField(
        'Service Name',
        validators=[DataRequired()]
    )

    odometer_reading = StringField(
        'Odometer Reading',
        validators=[DataRequired()]
    )

    part_sku = StringField(
        'Part SKU',
        validators=[DataRequired()]
    )

    submit = SubmitField('Upload')

class RunReport(FlaskForm):
    submit = SubmitField('Run')

class DemoItem():
    def __init__(self, name : str, local_link : str,
                    src_code_link: str, information : str,
                    authors: list, languages: list):
        if not(isinstance(name, str)
               and isinstance(local_link, str)
               and isinstance(information, str)
               and isinstance(src_code_link, str)
               and isinstance(authors, list)
               and isinstance(languages, list)):
            raise ValueError

        self.authors = authors
        self.demo_link = local_link
        self.base_link = 'static/demos'
        self.full_link = f'{self.base_link}/{self.demo_link}/runtime/driver.html'
        self.information = information
        self.languages = languages
        self.name = name
        self.src_code_link = src_code_link
