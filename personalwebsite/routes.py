from flask import Flask, render_template, url_for, flash, redirect, request, session, send_file, send_from_directory
from personalwebsite import app
from personalwebsite.models import PortfolioItem, GasolineCalculatorForm

GAS_PRICE = 2.5
MPG = 26
TANK = 15.5
MILES_MAX_AVAIL = MPG * TANK

def compute(current: int) -> float:
    """
    Compute the epsilon from max miles available (based on the tank size) and the current reading on the odometer
    This computation will result in miles, then subsquently dividing the number of "gallons" that the tank can theoretically hold.

    """
    gallon_epsilon = abs(MILES_MAX_AVAIL - current)/MPG
    cost = gallon_epsilon * GAS_PRICE
    return round(cost, 2)

@app.route("/")
@app.route("/home")
def home():
    diff_project = PortfolioItem(
        "delta",
        "A clone of the UNIX utility 'diff'",
        0,
        "/static/assets/diff.jpg",
        "https://google.com",
        "https://github.com/JaredDyreson/delta",
        "https://google.com"

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

    items = [diff_project, 
            starbucks_automa, 
            funnel_cake, 
            website]

    return render_template('portfolio.html', PortfolioItems=items)


@app.route("/about")
def about():
    return render_template('about.html', title = "About")

@app.route("/blog")
def blog():
    return render_template('blog.html', title = "Blog")

@app.route("/calculator", methods = ['GET', 'POST'])
def calculator():
    chonkulator = GasolineCalculatorForm(request.form)
    if(chonkulator.validate_on_submit()):
        GAS_PRICE = float(chonkulator.current_price.data)
        miles_to_e = int(chonkulator.current_miles_left.data)
        flash(f'Give the cashier ${compute(miles_to_e)}', 'success')
        return redirect(url_for('calculator'))
    return render_template('calculator.html', title = "Gas Calculator", form = chonkulator)
