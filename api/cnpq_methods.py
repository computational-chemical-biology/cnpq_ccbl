import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.mime.text import MIMEText

from selenium import webdriver
import chromedriver_binary
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time

import requests
from bs4 import BeautifulSoup

def seleniumReport():
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')

    driver = webdriver.Chrome(options=chrome_options)
    driver.get("http://memoria2.cnpq.br/web/guest/chamadas-publicas?p_p_id=resultadosportlet_WAR_resultadoscnpqportlet_INSTANCE_0ZaM&filtro=abertas/")
    WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.TAG_NAME, "h4")))
    time.sleep(1)
    titles = []
    txt = []
    dts = []
    #followers_els = driver.find_elements_by_css_selector(".item-value-data")
    title_els = driver.find_elements(By.TAG_NAME, "h4")
    for el in title_els:
        titles.append(el.text)

    txt_els = driver.find_elements(By.TAG_NAME, "p")
    for el in txt_els:
        txt.append(el.text)

    dts_els = driver.find_elements(By.CLASS_NAME, "datas")
    for el in dts_els:
        dts.append(el.text)

    return titles, txt, dts

def bs4Report():
    site = 'http://memoria2.cnpq.br/web/guest/chamadas-publicas?p_p_id=resultadosportlet_WAR_resultadoscnpqportlet_INSTANCE_0ZaM&filtro=abertas/'
    response = requests.get(site)
    soup = BeautifulSoup(response.text, 'html.parser')
    ol = soup.ol
    titles = [x.getText() for x in ol.findAll('h4')]
    description = [x.getText() for x in ol.findAll('p')]
    dates = [x.getText() for x in ol.find_all("ul", {"class": "datas"})]
    return titles, description, dates



def sendEmail(email, password, message, recipients,
              subject, fl=None):
        server = smtplib.SMTP('smtp.gmail.com', 587)
	#server.starttls()
        server.connect("smtp.gmail.com",587)
        server.ehlo()
        server.starttls()
        server.ehlo()
        server.login(email, password)
        recipients = ", ".join(recipients)

        msg = MIMEMultipart()
        msg['From'] = email
        msg['To'] = recipients
        msg['Subject'] = subject

        part1 = MIMEText(message, 'plain')
        msg.attach(part1)
        if fl:
            with open(fl, "rb") as fil:
                part = MIMEApplication(
                    fil.read(),
                    Name=basename(fl)
                )
            # After the file is closed
            part['Content-Disposition'] = 'attachment; filename="%s"' % basename(fl)
            msg.attach(part)

        server.sendmail(email, recipients, msg.as_string())
        server.quit()



