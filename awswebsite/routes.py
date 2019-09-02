from flask import Flask, render_template, url_for, flash, redirect, request, session, send_file, send_from_directory
from awswebsite import app
from awswebsite.models import User, Post

@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html', title="Home")


@app.route("/about")
def about():
    return render_template('about.html', title="About")

@app.route("/downloads", methods=['GET'])
def downloads():
	#assets_path = "assets/"
	#filename = "resume.pdf"
	#send_from_directory(assets_path, filename, as_attachment=True, mimetype='application/pdf', attachment_filename="{}.pdf".format(filename))

	return render_template('home.html', title="Home")
