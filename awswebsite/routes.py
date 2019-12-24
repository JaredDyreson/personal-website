from flask import Flask, render_template, url_for, flash, redirect, request, session, send_file, send_from_directory
from awswebsite import app
from awswebsite.forms import PostForm
from awswebsite.models import User, Post

@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html', title="Home")


@app.route("/about")
def about():
    return render_template('about.html', title="About")

@app.route("/post/new", methods=['GET', 'POST'])
def new_post():
	form = PostForm()
	if form.validate_on_submit():
		flash("Your post has been successfully created!", 'success')
		return redirect(url_for('home'))
	return render_template('create_post.html', title='New Post', form=form)

