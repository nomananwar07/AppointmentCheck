import requests
from bs4 import BeautifulSoup, NavigableString, Tag
import datetime
import json

from apscheduler.schedulers.blocking import BlockingScheduler


class Cookies:
    def __init__(self):
        self.cookies = {'TVWebSession': '3kqj8kopshjljs7au23uoj1afc	'}

    def get_cookies(self):
        return self.cookies

    def set_cookies(self, cook):
        self.cookies = cook

# cookie = Cookies()

def write_page(content, file_name):
    with open(file_name, "w") as file:
        file.write(str(content))


def Check_appointment():
    d = requests.get('https://termine.staedteregion-aachen.de/auslaenderamt/select2?md=1')
    c = d.cookies._cookies['.termine.staedteregion-aachen.de']['/auslaenderamt']['tvo_session'].value
    cookie = {'tvo_session': c}
    print ('cookie: {}'.format(c))

    content = BeautifulSoup(d.content, "html.parser")
    write_page(content, 'initial_page.html')


    headers = {"Cookie": "tvo_session={}; tvo_cookie_accept=0".format(c),
               "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
               "Content-Type": "application/x-www-form-urlencoded"}
    url = 'https://termine.staedteregion-aachen.de/auslaenderamt/location?mdt=78&select_cnc=1&cnc-204=0&cnc-205=0&cnc-198=1&cnc-201=0&cnc-202=0&cnc-227=0&cnc-232=0&cnc-203=0&cnc-196=0&cnc-190=0&cnc-185=0&cnc-187=0&cnc-188=0&cnc-186=0&cnc-192=0&cnc-191=0&cnc-194=0&cnc-197=0&cnc-193=0&cnc-183=0&cnc-184=0&cnc-195=0&cnc-200=0&cnc-228=0'

    r = requests.get(url, cookies=cookie, headers=headers)


    content = BeautifulSoup(r.content, "html.parser")
    write_page(content, 'select_location.html')

    today = datetime.datetime.now()

    if content.body.find(text='Kein freier Termin verfügbar'):
        msg = f"{today}: No appointment available"
    elif content.body.find('h1', attrs={"class": 'error'}) is not None:
        msg = f"{today}: Some Error occured"
        with open("error.html", "w") as file:
            file.write(str(content))
    else:
        # div, id=sugg_accordion
        payload = {}

        # print ('-----------Form printing---------')
        # forms = content.find_all('form')
        # for form in forms:
        #     print(form)
        #     print ('/n')
        #     print ('-----------Form printing---------')


        hidden = content.body.find('div', attrs = {'id':'suggest_location_content'}).find('form', attrs = {'method':'post'})
        for x in hidden:
            if isinstance(x, Tag) and all(k in x.attrs for k in ("name", "value")):
                payload[x['name']] = x["value"]


        print (payload)
        # payload = {x["name"]: x["value"] for x in hidden if x.contains('hidden')}






        r = requests.post(r.url, params=payload, cookies=cookie, headers=headers)
        print (r.status_code)
        print (r.url)



        r = requests.get("https://termine.staedteregion-aachen.de/auslaenderamt/suggest", cookies=cookie)
        print (r.status_code)
        print (r.url)

        content = BeautifulSoup(r.content, 'html.parser')
        write_page(content, 'final_page.html')




        dates = [i.text for i in content.body.find('div', attrs = {'id':'sugg_accordion'}).findAll('h3')]
        msg = f"{today}: Appointment Found,   Dates: {dates}"
        with open("found.html", "w") as file:
            file.write(str(content))

    print(msg)
    with open("logs.txt", "a") as file:
        file.write(msg+"\n")


Check_appointment()
scheduler = BlockingScheduler()
scheduler.add_job(Check_appointment, 'interval', hours=0.1)
scheduler.start()
