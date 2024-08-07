import celery
from celery.schedules import crontab
import os
import time
from datetime import datetime
import requests
from bs4 import BeautifulSoup
from config.settings import EMAIL, PASSWORD
from api.cnpq_methods import sendEmail
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
    site = 'http://memoria2.cnpq.br/web/guest/chamadas-publicas?p_p_id=resultadosportlet_WAR_resultadoscnpqportlet_INSTANCE_0ZaM&filtro=abertas/'

    response = requests.get(site)
    soup = BeautifulSoup(response.text, 'html.parser')
    ol = soup.ol
    titles = [x.getText() for x in ol.findAll('h4')]
    description = [x.getText() for x in ol.findAll('p')]
    dates = [x.getText() for x in ol.find_all("ul", {"class": "datas"})]

    old_html = 'api/data/chamadas_abertas.html'

    if os.path.isfile(old_html):
        with open(old_html) as f:
            txt = f.read()
        old_soup = BeautifulSoup(txt, 'html.parser')
        old_ol = old_soup.ol
        old_titles = [x.getText() for x in old_ol.findAll('h4')]
    else:
        old_titles = []

    if set(titles)-set(old_titles):
        msg = []
        for i in range(len(dates)):
            msg.append('\n'.join([titles[i], description[i], dates[i]]))
        msg.append(site)
        msg = '\n'.join(msg)
        subject = 'CNPq grant update'
        for x in db.session.query(Recipient).all():
            utxt = f'Click here<http://ccbl.fcfrp.usp.br:5050/unsubscribe/{x.id}> to unsubscribe.'
            umsg = msg+'\n'+utxt
            sendEmail(EMAIL, PASSWORD, umsg, [x.email], subject)
        with open(old_html, "w+") as f:
            f.write(str(ol))

# add "watchdog" task to the beat schedule
app.conf.beat_schedule = {
    "scan_twitter-task": {
        "task": "scan_cnpq",
         #"schedule": crontab(minute="*/10")
        "schedule": crontab(minute="10", hour="15", day_of_week='*',
                            day_of_month='*', month_of_year='*')
    }
}

