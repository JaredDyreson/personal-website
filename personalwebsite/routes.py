from flask import Flask, render_template, url_for, flash, redirect, request, session, send_file, send_from_directory

from werkzeug.utils import secure_filename

from personalwebsite import app
from personalwebsite.models import PortfolioItem, GasolineCalculatorForm, BlogItem, BlogCategory, ServiceForm, RunReport, DemoItem
from personalwebsite.BlogStructure import BlogHierarchy, DEFAULT_BUILD
from personalwebsite.MarkdownParser import Markdown
from personalwebsite.carutils import service, inventory

import pathlib
import os
import sqlite3
from datetime import datetime
import shutil

GAS_PRICE = 2.5
MPG = 26
TANK = 15.5
MILES_MAX_AVAIL = MPG * TANK

path = pathlib.Path(os.path.join(app.root_path, "blog"))
Blog = BlogHierarchy(path)

ALLOWED_EXTENSIONS = {'.gpg'}


def compute(current: int) -> float:
    """
    Compute the epsilon from max miles available (based on the tank size) and the current reading on the odometer
    This computation will result in miles, then subsquently dividing the number of "gallons" that the tank can theoretically hold.

    """
    gallon_epsilon = abs(MILES_MAX_AVAIL - current)/MPG
    cost = gallon_epsilon * GAS_PRICE
    return round(cost, 2)

def build_structure():
    blog_posts, all_categories = [], []
    structure = Blog.structure['']

    for category in structure:
        content = structure[category]
        all_categories.append(category)
        if(isinstance(content, list)):
            for instance in content:
                instance_path = pathlib.Path(os.path.join(path.name, category, instance))
                blog_posts.append(Markdown(instance_path.absolute()))
        else:
            for subcategory in content:
                subcontent = structure[category][subcategory]
                for instance in subcontent:
                    instance_path = pathlib.Path(os.path.join(path.name, category, subcategory, instance))
                    blog_posts.append(Markdown(instance_path.absolute()))

    blog_posts = [BlogItem(post) for post in blog_posts]
    return (blog_posts, all_categories)

BLOG_POSTS, BLOG_CATEGORIES = build_structure()

def search_posts(params: tuple):
    cat, subcat, name = params
    for post in BLOG_POSTS:
        c, s, n = post.subcategory, post.category, post.file_name
        if(c == cat and s == subcat and n.split()[0] == n):
            return post
    return None


def allowed_file(filename):
    if not(isinstance(filename, pathlib.Path)):
        raise ValueError

    return filename.suffix in ALLOWED_EXTENSIONS


@app.route("/")
@app.route("/home")
def home():

    # return render_template('portfolio.html', PortfolioItems=items)
    return render_template('index.html')


@app.route("/about")
def about():
    return render_template('about.html', title = "About")

# @app.route("/blog")
# def blog():
    # data_structures = BlogCategory(
        # "data_structures",
        # "/static/assets/blog_categories/data_structures.png",
        # "Computer Science data structure tutorials"
    # )
    # linux = BlogCategory(
        # "linux",
        # "/static/assets/blog_categories/linux.png",
        # "All things Linux related"
    # )

    # scripting = BlogCategory(
        # "scripting",
        # "/static/assets/blog_categories/scripting.png",
        # "Learn how to automate tedious proceses with different scripting languages"
    # )

    # workflow = BlogCategory(
        # "workflow",
        # "/static/assets/blog_categories/notes.jpeg",
        # "Learn how to improve your workflow with some tips"
    # )

    # items = [
        # data_structures,
        # linux,
        # scripting,
        # workflow
    # ]
    # return render_template('blog_categories.html', BlogCategories=items, title = "Blog")

@app.route("/blog/<category>")
def blogcategories(category):
    return render_template('blog.html', BlogItems=[post for post in BLOG_POSTS if post.subcategory == category])

@app.route("/blog/<category>/<subcategory>")
def blogpage(category, subcategory):
    return render_template('blog.html', BlogItems=[post for post in BLOG_POSTS if post.category == subcategory])

@app.route("/blog/<category>/<subcategory>/<article>")
def blogarticle(category, subcategory, article):
    found = search_posts((category, subcategory, article))
    if(found):
        return render_template('blog_landing_page.html', BI=found)
    return redirect(url_for('calculator'))


@app.route('/car', methods=['GET', 'POST'])
def car():
    service_window = ServiceForm(request.form)
    reporter = RunReport(request.form)
    chonkulator = GasolineCalculatorForm(request.form)

    if(service_window.validate_on_submit()):
        print("this one got push")
        name = service_window.service_name.data
        reading = service_window.odometer_reading.data
        sku = service_window.part_sku.data
        if('file' not in request.files):
            print("file not here")
            flash('No file part', 'error')
            return redirect(request.url)

        file = request.files['file']
        path = file.filename
        mime = os.path.basename(file.mimetype)

        if not(path):
            print("no file has been selected")
            flash('File has not been selected', 'error')
            return redirect(request.url)
        if(mime == "pgp-encrypted"):
            filename = secure_filename(path)
            destination = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(destination)

            database_path = pathlib.Path("services.db")
            connection = sqlite3.connect(database_path)
            Invent = inventory.Inventory(connection)
            new_service = service.Service(
                name,
                datetime.now(),
                float(reading),
                sku,
                pathlib.Path(destination)
            )
            Invent.insert_service(new_service)
            Invent.connection.commit()
            flash(f'Successfully add {name}', 'success')
            return redirect(url_for('car'))
    elif(reporter.validate_on_submit()):
        return redirect(url_for('report'))

    elif(chonkulator.validate_on_submit()):
        GAS_PRICE = float(chonkulator.current_price.data)
        miles_to_e = int(chonkulator.current_miles_left.data)
        flash(f'Give the cashier ${compute(miles_to_e)}', 'success')
        return redirect(url_for('car'))

    return render_template('car_landing.html', title = "Car Tools", form = service_window, run_report = reporter, calculator = chonkulator)

@app.route('/car/report', methods=['GET', 'POST'])
def report():
    database_path = pathlib.Path("services.db")
    connection = sqlite3.connect(database_path)
    Invent = inventory.Inventory(connection)
    packet = []

    for element in Invent.get_all_services():
        name, date, reading, sku, path = element
        packet.append(service.Service(name, date, float(reading), sku, pathlib.Path(path)))
    return render_template('car_report.html', items = packet)

@app.route("/demos")
def demos():
    # 335 Siska Projects

    cella_ant = DemoItem(
        "Cella Ant 0x15",
        "Cella-Ant",
        "https://github.com/JaredDyreson/Cella-Ant-x15",
        "A cellular automaton variant of Langton's Ant",
        ["Jared Dyreson", "Mason Godfrey"],
        ["CSS", "HTML", "Javascript"]
    )

    sorting_olympics = DemoItem(
        "Sorting Olympics",
        "Sorting-Olympics",
        "https://github.com/JaredDyreson/Sorting-Olympics",
        "Sorting algorithm comparision program",
        ["Jared Dyreson", "Mason Godfrey"],
        ["CSS", "HTML", "Javascript"]
    )

    balloon_juice = DemoItem(
        "Balloon Juice",
        "Balloon-Juice",
        "https://github.com/JaredDyreson/Ballon-Juice/",
        "Mission reconnaissance visualizer, showing a bot retrieve a balloon in a deeply nested balloon field",
        ["Jared Dyreson", "Mason Godfrey"],
        ["CSS", "HTML", "Javascript"]
    )

    items = [
        cella_ant,
        sorting_olympics,
        # balloon_juice
    ]

    categories = {
        "Javascript": items
    }
    return render_template('demos.html', Demos=items)

@app.route("/projects")
def projects():
    tuffix = PortfolioItem(
        "Tuffix",
        "Official Linux development environment for CSUF",
        "/static/assets/portfolio_items/tuffix.png",
        "https://github.com/mshafae/tuffix",
        "https://github.com/mshafae/tuffix/wiki",
        ["Michael Shafae", "Kevin Wortman", "Paul Inventado", "Jared Dyreson"],
        ["Python 3.8"]
    )

    starbucks_automa = PortfolioItem(
        "Starbucks Automa",
        "Auto work scheduler for the Starbucks Partner Portal",
        "/static/assets/portfolio_items/starbucks_coffee_robot_wallpaper-t2.jpg",
        "https://jareddyreson.github.io/posts/starbucks_automa_documentation.html",
        "https://github.com/JaredDyreson/starbucks_automa_production",
        ["Jared Dyreson"],
        ["Python 3.8", "HTML", "CSS"]
    )

    funnel_cake = PortfolioItem(
        "Funnel Cake",
        "Utility for managing Spotify playlists",
        "/static/assets/portfolio_items/funnel_cake.jpg",
        # "#", # TODO : demo link for Funnel Cake
        "https://github.com/JaredDyreson/Spoterm/blob/master/flask_stuff/DOCUMENTATION.md", # TODO : more readable documentation
        "https://github.com/jareddyreson/funnel-cake",
        ["Jared Dyreson"],
        ["Python 3.8"]
    )

    website = PortfolioItem(
        "Personal Website",
        "A place to host portfolio items and show a little about me",
        "/static/assets/portfolio_items/python-bottle-aws-1.width-808.jpg",
        # "https://www.jareddyreson.xyz",
        "#", # TODO: documentation about the site?
        "https://github.com/JaredDyreson/personal-website",
        ["Jared Dyreson"],
        ["Python 3.8", "HTML", "CSS"]
    )

    bauer = PortfolioItem(
        "Bauer",
        "Reverse Polish Notation Calculator",
        "/static/assets/portfolio_items/bauer.jpg",
        # "#", # TODO : demo of Bauer
        "https://github.com/JaredDyreson/RPN-Calculator/blob/master/README.md",
        "https://github.com/JaredDyreson/RPN-Calculator",
        ["Jared Dyreson", "Sergio Herrera"],
        ["Python 3.8", "Javascript", "HTML", "CSS"]

    )
    items = [tuffix,
            bauer,
            starbucks_automa,
            funnel_cake,
            website]
    return render_template('portfolio.html', PortfolioItems=items)
