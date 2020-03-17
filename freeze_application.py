#!/usr/bin/env python3.8

from flask_frozen import Freezer
from awswebsite import app

freezer = Freezer(app)

if __name__ == '__main__':
    freezer.freeze()

