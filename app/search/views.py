from flask import render_template, redirect, request, url_for, flash, current_app
from flask_login import login_required, current_user
from sqlalchemy import or_
from .. import db
from . import search
from ..models import Post, User
import random
import requests
import re


@search.route('/explore')
def explore():
    # generate an random num
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) \
     Chrome/70.0.3538.110 Safari/537.36'
    }
    while True:
        problemID = random.randint(1000, 2000)  # random a problem id
        url = 'http://www.51nod.com/Challenge/Problem?problemId={0}'.format(problemID)
        # print(url)
        t = requests.get(url=url, headers=headers)
        content = t.content.decode()
        if len(content) >100:
            break
    print(problemID)
    # title
    title_pattern = '"Title":"(.*?)","IsPay"'
    title = re.findall(pattern=title_pattern, string=content)
    title = title[0].replace('\\n','\n')

    # problem_description
    descripion_pattern = '"Description":"(.*?)","InputDescription'
    descripion = re.findall(pattern=descripion_pattern, string=content)
    descripion = descripion[0].replace('\\n','\n')

    # input_desription
    input_pattern = '"InputDescription":"(.*?)","OutputDescription"'
    input_description = re.findall(pattern=input_pattern, string=content)
    input_description = input_description[0].replace('\\n','\n')

    # output_description
    output_pattern = '"OutputDescription":"(.*?)","InputSample"'
    output_descrition = re.findall(pattern=output_pattern, string=content)
    output_descrition = output_descrition[0].replace('\\n','\n')

    # input_sample
    input_pattern = '"InputSample":"(.*?)","OutputSample"'
    input_sample = re.findall(pattern=input_pattern, string=content)
    input_sample = input_sample[0].replace('\\n','\n').strip()

    # output_sample
    output_pattern = '"OutputSample":"(.*?)","TimeLimit":'
    output_sample = re.findall(pattern=output_pattern, string=content)
    output_sample = output_sample[0].replace('\\n','\n').strip()
    problemUrl='http://www.51nod.com/Challenge/Problem.html#!#problemId={0}'.format(problemID)
    return render_template('search/problem_show.html',title=title,descripion=descripion,
                           input_description=input_description,
                           output_descrition=output_descrition,input_sample=input_sample,
                           output_sample=output_sample,url=problemUrl)


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
