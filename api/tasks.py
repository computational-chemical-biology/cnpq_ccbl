import celery
from celery.schedules import crontab
import os
import time
from datetime import datetime
from config.settings import EMAIL, PASSWORD
from api.cnpq_methods import sendEmail
from api.cnpq_methods import seleniumReport
from api import db
from api.models import Recipient

#app = celery.Celery('tasks', backend='redis://localhost:6379/0',
#                    broker='redis://localhost:6379/0')

app = celery.Celery('tasks', backend='redis://redis:6379/0',
                broker='redis://redis:6379/0')

@app.task(name='scan_cnpq')
def scan_cnpq():
    # Chamadas Públicas abertas
    print('Scanning cnpq %s' % datetime.now().strftime("%m/%d/%Y, %H:%M:%S"))
    titles, description, dates = seleniumReport()
    old_txt = 'api/data/chamadas_abertas.txt'

    if os.path.isfile(old_txt):
        with open(old_txt) as f:
            old_titles = [title.rstrip() for title in f]
    else:
        old_titles = []

    if set(titles)-set(old_titles):
        msg = []
        for i in range(len(dates)):
            msg.append('\n'.join([titles[i], dates[i]]))
        msg.append(site)
        msg = '\n'.join(msg)
        subject = 'CNPq grant update'
        for x in db.session.query(Recipient).all():
            utxt = f'Click here<http://ccbl.fcfrp.usp.br:5050/unsubscribe/{x.id}> to unsubscribe.'
            umsg = msg+'\n'+utxt
            sendEmail(EMAIL, PASSWORD, umsg, [x.email], subject)
        with open(old_txt, "w+") as f:
            for title in titles:
                f.write(f"{title}\n")

# add "watchdog" task to the beat schedule
app.conf.beat_schedule = {
    "scan_twitter-task": {
        "task": "scan_cnpq",
         #"schedule": crontab(minute="*/10")
        "schedule": crontab(minute="10", hour="15", day_of_week='*',
                            day_of_month='*', month_of_year='*')
    }
}

