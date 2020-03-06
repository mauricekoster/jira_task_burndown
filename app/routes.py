import copy
import csv
import os
from pprint import pprint

from flask import render_template, jsonify, flash, redirect

from app import app
from app.forms import LoginForm


@app.route('/index')
def index():
    return "Hello, World!"

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash('Login requested for user {}, remember_me={}'.format(
            form.username.data, form.remember_me.data))
        return redirect('/index')
    return render_template('login.html', title='Sign In', form=form)

@app.route("/")
def chart():
    return render_template('chart.html', sprint='Sprint 2020.1.5')


def get_data_from_file(fn):
    dataset = {
        'label': 'template',
        'fill': False,
        'lineTension': 0.1,
        'backgroundColor': "rgba(75,192,192,0.4)",
        'borderColor': "rgba(75,192,192,1)",
        'borderCapStyle': 'butt',
        'borderDash': [],
        'borderDashOffset': 0.0,
        'borderJoinStyle': 'miter',
        'pointBorderColor': "rgba(75,192,192,1)",
        'pointBackgroundColor': "#fff",
        'pointBorderWidth': 1,
        'pointHoverRadius': 5,
        'pointHoverBackgroundColor': "rgba(75,192,192,1)",
        'pointHoverBorderColor': "rgba(220,220,220,1)",
        'pointHoverBorderWidth': 2,
        'pointRadius': 1,
        'pointHitRadius': 10,
        'data': [],
        'spanGaps': False
    }

    labels = []
    guard_line_data_set = copy.deepcopy(dataset)
    guard_line_data_set['label'] = 'Guard Line'
    guard_line_data_set['borderColor'] = "rgb(38, 153, 0)"
    storypoints_data_set = copy.deepcopy(dataset)
    storypoints_data_set['label'] = 'Storypoints'
    storypoints_data_set['borderColor'] = "rgb(242, 47, 171)"
    open_storypoints_data_set = copy.deepcopy(dataset)
    open_storypoints_data_set['label'] = 'Open storypoints'
    open_storypoints_data_set['borderColor'] = "rgb(242, 242, 47)"

    tasks_data_set = copy.deepcopy(dataset)
    tasks_data_set['label'] = 'Tasks'
    tasks_data_set['borderColor'] = "rgb(47, 73, 242)"
    open_tasks_data_set = copy.deepcopy(dataset)
    open_tasks_data_set['label'] = 'Open tasks'
    open_tasks_data_set['borderColor'] = "rgb(47, 171, 242)"

    if os.path.exists(fn):
        with open(fn) as csvfile:
            reader = csv.DictReader(csvfile, delimiter=';')
            for row in reader:
                labels.append(row['label'])
                guard_line_data_set['data'].append(row['guide line'])
                v = row['storypoints']
                if v:
                    storypoints_data_set['data'].append(v)
                v = row['open storypoints']
                if v:
                    open_storypoints_data_set['data'].append(v)
                v = row['tasks']
                if v:
                    tasks_data_set['data'].append(v)
                v = row['open tasks']
                if v:
                    open_tasks_data_set['data'].append(v)
    return {
        'labels': labels,
        'datasets': [guard_line_data_set,
                     storypoints_data_set, open_storypoints_data_set,
                     tasks_data_set, open_tasks_data_set]
    }


@app.route('/api/data')
def get_data():
    basedir = os.path.abspath(os.path.dirname(__file__))
    data = get_data_from_file(os.path.join(basedir, 'data.csv'))
    pprint(data)
    chart_data = {
        'type': 'line',
        'data': data
    }
    return jsonify(chart_data)

