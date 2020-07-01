"""
Using Font Awesome in HTML:
https://www.w3schools.com/icons/fontawesome_icons_intro.asp

Search font awesome icons:
https://fontawesome.com/v4.7.0/icons/

"""


class PortfolioItem():
    def __init__(self, title: str, content: str, number: int, 
                    image_path: str, demo_link: str, doc_link: str, src_link : str):
        self.title_ = title
        self.content = content
        self.number = number
        self.image_path = image_path
        self.demo_link = demo_link
        self.doc_link = doc_link
        self.src_link = src_link
