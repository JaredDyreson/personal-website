from flask import Flask, render_template, url_for, flash, redirect, request, session, send_file, send_from_directory
from awswebsite import app
from awswebsite.forms import PostForm
from awswebsite.models import PortfolioItem

@app.route("/")
@app.route("/home")
def home():
  starbucks_automa = PortfolioItem(
      "Starbucks Automa",
      "Auto scheduler for the Starbucks Partner Portal",
       0,
      "https://www.freecomputerwallpapers.net/thumbs/starbucks_coffee_robot_wallpaper-t2.jpg",
      "https://asciinema.org/a/9m8kAz6O45TyPMPAU34Hivtiv?t=1",
      "https://jareddyreson.github.io/posts/starbucks_automa_documentation.html",
      "https://github.com/JaredDyreson/starbucks_automa_production"
  )
  funnel_cake = PortfolioItem(
      "Funnel Cake",
      "Utility for managing Spotify playlists",
       1,
      "https://jareddyreson.github.io/images/funnel_cake.jpg",
      "http://funnelcake-env.s29abpc9ge.us-west-1.elasticbeanstalk.com/",
      "https://github.com/JaredDyreson/Spoterm/blob/master/flask_stuff/DOCUMENTATION.md",
      "https://github.com/jareddyreson/funnel-cake"
  )
  return render_template('portfolio.html', PortfolioItems=[starbucks_automa, funnel_cake])


@app.route("/about")
def about():
    return render_template('about.html', title="About")
