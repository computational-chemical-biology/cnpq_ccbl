#!/usr/bin/env python
from flask import Flask, render_template, request, url_for, redirect
from flask_bootstrap import Bootstrap
from api.models import JournalForm
import json
#from api.twitter_methods import update_journals
import os

class Config(object):
    SECRET_KEY = '78w0o5tuuGex5Ktk8VvVDF9Pw3jv1MVE'

application = Flask(__name__)
application.config.from_object(Config)

Bootstrap(application)

@application.route('/', methods=['GET', 'POST'])
def update_journal():
    form = JournalForm(request.form)
    if not form.validate_on_submit():
        return render_template('add_handle.html', form=form)
    if request.method == 'POST':
        update_journals(form.journal_name.data, form.twitter.data)
        return redirect(url_for('journals'))

@application.route('/journals')
def journals():
    with open('api/data/journals.json') as f:
        journals = json.load(f)
    response = application.response_class(
        response=json.dumps(journals),
        status=200,
        mimetype='application/json'
    )
    return response

@application.route('/twetes')
def twetes():
    if os.path.isfile('api/data/old_twetes.json'):
        with open('api/data/old_twetes.json') as f:
            old_twetes = json.load(f)
    else:
        old_twetes = {}
    response = application.response_class(
        response=json.dumps(old_twetes),
        status=200,
        mimetype='application/json'
    )
    return response



if __name__ == '__main__':
    application.run()
    #application.run(host='0.0.0.0', debug=True)
