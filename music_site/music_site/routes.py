from flask import render_template, url_for, flash, redirect

from . import app
from .models import User


@app.route('/')
def index():
    return 'Hello world'
