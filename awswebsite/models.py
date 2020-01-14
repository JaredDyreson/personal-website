from awswebsite import db
from datetime import datetime

class User(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(20), unique=True, nullable=False)
	email = db.Column(db.String(120), unique=True, nullable=False)
	image_file = db.Column(db.String(20), nullable=False, default="default.jpg")
	password = db.Column(db.String(60), nullable=False)
	posts = db.relationship('Post', backref='author', lazy=True)	
	portfolio_items = db.relationship('PortfolioItem', backref='author', lazy=True)
	def __repr__(self):
		return "User({}, {}, {})".format(self.username, self.email, self.image_file)


class Post(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(100), nullable=False)
	date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
	# always use UTC
	content = db.Column(db.Text, nullable=False)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
	category = db.Column(db.String(50), nullable=False)

	def __repr__(self):
		return "Post({}, {}, category={})".format(self.title, self.date_posted, self.category)
class Category(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	content = db.Column(db.Text, nullable=False)
	name = db.Column(db.String(50), nullable=False)

	def __repr__(self):
		return "Category({})".format(name)
class PortfolioItem(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(100), nullable=False)
	content = db.Column(db.Text, nullable=False)
	demo_link = db.Column(db.String(100), nullable=False)
	source_link = db.Column(db.String(100), nullable=False)
	documentation_link = db.Column(db.String(100), nullable=False)
	image_file = db.Column(db.String(20), nullable=False, default="default.jpg")
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
	
	def __repr__(self):
		return "PortfolioItem({}, {}, {}, {})".format(self.title, self.demo_link, self.source_link, self.documentation_link, self.image_file)

