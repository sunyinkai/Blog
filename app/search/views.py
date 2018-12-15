from flask import render_template, redirect, request, url_for, flash
from flask_login import login_required, current_user
from sqlalchemy import or_
from .. import db
from . import search
from ..models import Post


@search.route('/search')
def search():
    keyword = request.args.get('keyword')
    posts = Post.query.filter(or_(Post.title.contains(keyword),
                                  Post.body.contains(keyword))).order_by(Post.timestamp.desc()).all()
    return render_template('search/result.html',
                           post_set=posts)  # this place is is post_set -> posts will be wrong!!why
