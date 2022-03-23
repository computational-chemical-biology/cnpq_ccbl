#!/usr/bin/env python
from flask import Flask, render_template, request, url_for, redirect, flash
from flask_bootstrap import Bootstrap
from api.forms import RecipientForm
import json
#from api.twitter_methods import update_journals
import os
from config.settings import EMAIL, PASSWORD
from api.cnpq_methods import sendEmail

from api import application, db
from api.models import Recipient

Bootstrap(application)

@application.before_first_request
def create_tables():
    db.create_all()

@application.route('/', methods=['GET', 'POST'])
def update_recipient():
    form = RecipientForm(request.form)
    if not form.validate_on_submit():
        return render_template('add_handle.html', form=form)
    if request.method == 'POST':
        recipient = Recipient()
        recipient.name = form.name.data
        recipient.email = form.email.data
        db.session.add(recipient)
        db.session.commit()

        flash('Contact was successfully added')
        subject = 'CNPq grant track subscription'
        msg = f'Dear {form.name.data},\nyour subscription is confirmed.'
        sendEmail(EMAIL, PASSWORD, msg, [form.email.data], subject)
        return redirect(url_for('update_recipient'))

#if __name__ == '__main__':
#    application.run()
#    application.run(host='0.0.0.0', debug=True)
