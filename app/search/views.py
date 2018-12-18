from flask import render_template, redirect, request, url_for, flash, current_app
from flask import session
from flask_login import login_required, current_user
from sqlalchemy import or_
from .. import db
from . import search
from ..models import Post, User, Problem
import random
import requests
import re


def add_to_database(problem_id):
    url = 'http://www.51nod.com/Challenge/Problem?problemId={0}'.format(problem_id)
    # print(url)
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) \
     Chrome/70.0.3538.110 Safari/537.36'
    }
    t = requests.get(url=url, headers=headers)
    content = t.content.decode()
    # title
    title_pattern = '"Title":"(.*?)","IsPay"'
    title = re.findall(pattern=title_pattern, string=content)
    title = title[0].replace('\\n', '\n')

    # problem_description
    descripion_pattern = '"Description":"(.*?)","InputDescription'
    descripion = re.findall(pattern=descripion_pattern, string=content)
    descripion = descripion[0].replace('\\n', '\n')

    # input_desription
    input_pattern = '"InputDescription":"(.*?)","OutputDescription"'
    input_description = re.findall(pattern=input_pattern, string=content)
    input_description = input_description[0].replace('\\n', '\n')

    # output_description
    output_pattern = '"OutputDescription":"(.*?)","InputSample"'
    output_descrition = re.findall(pattern=output_pattern, string=content)
    output_descrition = output_descrition[0].replace('\\n', '\n')

    # input_sample
    input_pattern = '"InputSample":"(.*?)","OutputSample"'
    input_sample = re.findall(pattern=input_pattern, string=content)
    input_sample = input_sample[0].replace('\\n', '\n').strip()

    # output_sample
    output_pattern = '"OutputSample":"(.*?)","TimeLimit":'
    output_sample = re.findall(pattern=output_pattern, string=content)
    output_sample = output_sample[0].replace('\\n', '\n').strip()
    t = Problem(id=problem_id, isok=True, title=title, description=descripion,
                input_description=input_description, output_description=output_descrition,
                input_sample=input_sample, output_sample=output_sample)
    db.session.add(t)
    db.session.commit()


@search.route('/explore')
def explore():
    # generate an random num
    while True:
        if (request.args.get('flag') is None) and (session.get('problem_id') is not None):
            problem_id = session.get('problem_id')
            break

        problem_id = random.randint(1000, 1500)  # random a problem id
        problem = Problem.query.filter_by(id=problem_id).first()
        print(problem)
        print(problem_id)
        if problem is None:  # database has no such id
            pass
        elif problem.isok == False:  # the problem is bad
            continue
        elif problem.isok:  # the problem is ok
            break
        url = 'http://www.51nod.com/Challenge/Problem?problemId={0}'.format(problem_id)
        # print(url)
        headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) \
         Chrome/70.0.3538.110 Safari/537.36'
        }
        t = requests.get(url=url, headers=headers)
        print(t)
        content = t.content.decode()
        if len(content) > 100:
            break
        else:
            t = Problem(id=problem_id, isok=False)
            db.session.add(t)
            db.session.commit()
    # write the problem_id to the session the avoid flush
    flag = request.args.get('flag')
    # session is NULL:the first time to visit this page
    # flag is not None:visit this page by click change the problem
    if (flag is not None) or (session.get('problem_id') is None):
        session['problem_id'] = problem_id
        return redirect('http://localhost:5000/explore')
    else:
        problem_id = session['problem_id']  # else use the problem in the session

    print(problem_id)
    problem = Problem.query.filter_by(id=problem_id).first()
    if problem is None:  # if database has no such id,add to database
        add_to_database(problem_id)
    problem = Problem.query.filter_by(id=problem_id).first()
    title = problem.title
    descripion = problem.description
    input_description = problem.input_description
    output_descrition = problem.output_description
    input_sample = problem.input_sample
    output_sample = problem.output_sample

    problemUrl = 'http://www.51nod.com/Challenge/Problem.html#!#problemId={0}'.format(problem_id)
    return render_template('search/problem_show.html', title=title, descripion=descripion,
                           input_description=input_description,
                           output_descrition=output_descrition, input_sample=input_sample,
                           output_sample=output_sample, url=problemUrl, problem_id=problem_id)


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
