from flask import Flask, render_template, redirect, session, url_for, flash
from .. import db
from ..models import User
from . import main
from .forms import NameForm
@main.route('/')
def index():
	return render_template('index.html')