from flask import render_template, redirect, request, url_for, flash,current_app
from flask_login import login_required, current_user
from sqlalchemy import or_
from .. import db
from . import search
from ..models import Post,User


@search.route('/search')
def search():
    keyword = request.args.get('keyword')
    page = request.args.get('page', 1, type=int)
    pagination = Post.query.filter(or_(Post.title.contains(keyword),
                                  Post.body.contains(keyword))).order_by(Post.timestamp.desc()).paginate(
        page, per_page=current_app.config['FLASKY_POSTS_PER_PAGE'], error_out=False
    )
    posts = pagination.items
    return render_template('search/result.html',
                           post_set=posts, pagination=pagination)
