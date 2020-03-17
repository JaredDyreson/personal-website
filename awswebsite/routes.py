from flask import Flask, render_template, url_for, flash, redirect, request, session, send_file, send_from_directory
from awswebsite import app
from awswebsite.forms import PostForm
from awswebsite.models import PortfolioItem

@app.route("/")
@app.route("/home")
def home():
  cpsc_223C_exam = PortfolioItem(
      "CPSC-223C Exam One Coding",
      "Coding assignment for CPSC-223C Exam 1 (Click Source Code)",
       0,
      "/static/assets/C_progamming.png",
      "https://google.com",
      "https://google.com",
      "https://github.com/JaredDyreson/C-Programming/blob/master/exam_one/code_for_exam.c"
  )
  starbucks_automa = PortfolioItem(
      "Starbucks Automa",
      "Auto work scheduler for the Starbucks Partner Portal",
       1,
      "/static/assets/starbucks_coffee_robot_wallpaper-t2.jpg",
      "https://asciinema.org/a/9m8kAz6O45TyPMPAU34Hivtiv?t=1",
      "https://jareddyreson.github.io/posts/starbucks_automa_documentation.html",
      "https://github.com/JaredDyreson/starbucks_automa_production"
  )
  funnel_cake = PortfolioItem(
      "Funnel Cake",
      "Utility for managing Spotify playlists",
       2,
      "/static/assets/funnel_cake.jpg",
      "http://funnelcake-env.s29abpc9ge.us-west-1.elasticbeanstalk.com/",
      "https://github.com/JaredDyreson/Spoterm/blob/master/flask_stuff/DOCUMENTATION.md",
      "https://github.com/jareddyreson/funnel-cake"
  )

  website = PortfolioItem(
      "Personal Website",
      "A place to host portfolio items and show a little about me",
       3,
      "/static/assets/python-bottle-aws-1.width-808.jpg",
      "http://jareddyreson.com",
      "https://google.com",
      "https://github.com/JaredDyreson/aws-website"

  )

  return render_template('portfolio.html', PortfolioItems=[cpsc_223C_exam, starbucks_automa, funnel_cake, website])


@app.route("/about")
def about():
    return render_template('about.html', title="About")
