from flask import Flask, render_template, url_for, flash, redirect, request, session, send_file, send_from_directory
from personalwebsite import app
from personalwebsite.models import PortfolioItem, GasolineCalculatorForm, BlogItem, BlogCategory
from personalwebsite.BlogStructure import BlogHierarchy, DEFAULT_BUILD
from personalwebsite.MarkdownParser import Markdown
import pathlib
import os

GAS_PRICE = 2.5
MPG = 26
TANK = 15.5
MILES_MAX_AVAIL = MPG * TANK

path = pathlib.Path(os.path.join(app.root_path, "blog"))
Blog = BlogHierarchy(path)

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


@app.route("/")
@app.route("/home")
def home():
    diff_project = PortfolioItem(
        "Tuffix",
        "Official Linux environment for CPSC 120, 121, and 131 at California State University, Fullerton (contributor to this project)",
        0,
        "/static/assets/portfolio_items/diff.jpg",
        "https://github.com/mshafae/tuffix/wiki",
        "https://github.com/mshafae/tuffix",
        "https://google.com"

    )
    starbucks_automa = PortfolioItem(
        "Starbucks Automa",
        "Auto work scheduler for the Starbucks Partner Portal",
        1,
        "/static/assets/portfolio_items/starbucks_coffee_robot_wallpaper-t2.jpg",
        "https://asciinema.org/a/9m8kAz6O45TyPMPAU34Hivtiv?t=1",
        "https://jareddyreson.github.io/posts/starbucks_automa_documentation.html",
        "https://github.com/JaredDyreson/starbucks_automa_production"
    )
    funnel_cake = PortfolioItem(
        "Funnel Cake",
        "Utility for managing Spotify playlists",
        2,
        "/static/assets/portfolio_items/funnel_cake.jpg",
        "http://funnelcake-env.s29abpc9ge.us-west-1.elasticbeanstalk.com/",
        "https://github.com/JaredDyreson/Spoterm/blob/master/flask_stuff/DOCUMENTATION.md",
        "https://github.com/jareddyreson/funnel-cake"
    )

    website = PortfolioItem(
        "Personal Website",
        "A place to host portfolio items and show a little about me",
        3,
        "/static/assets/portfolio_items/python-bottle-aws-1.width-808.jpg",
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
    data_structures = BlogCategory(
        "data_structures",
        "/static/assets/blog_categories/data_structures.png",
        "Computer Science data structure tutorials"
    )
    linux = BlogCategory(
        "linux",
        "/static/assets/blog_categories/linux.png",
        "All things Linux related"
    )

    scripting = BlogCategory(
        "scripting",
        "/static/assets/blog_categories/scripting.png",
        "Learn how to automate tedious proceses with different scripting languages"
    )

    workflow = BlogCategory(
        "workflow",
        "/static/assets/blog_categories/scripting.png",
        "Learn how to improve your workflow with some tips"
    )

    items = [
        data_structures,
        linux,
        scripting,
        workflow
    ]
    return render_template('blog_categories.html', BlogCategories=items, title = "Blog")

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

@app.route("/calculator", methods = ['GET', 'POST'])
def calculator():
    chonkulator = GasolineCalculatorForm(request.form)
    if(chonkulator.validate_on_submit()):
        GAS_PRICE = float(chonkulator.current_price.data)
        miles_to_e = int(chonkulator.current_miles_left.data)
        flash(f'Give the cashier ${compute(miles_to_e)}', 'success')
        return redirect(url_for('calculator'))
    return render_template('calculator.html', title = "Gas Calculator", form = chonkulator)
