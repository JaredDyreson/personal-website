from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


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

        self.title_ = title
        self.content = content
        self.number = number
        self.image_path = image_path
        self.demo_link = demo_link
        self.doc_link = doc_link
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
