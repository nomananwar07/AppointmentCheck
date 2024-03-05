import datetime
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from apscheduler.schedulers.blocking import BlockingScheduler


def Check_appointment():
    option = webdriver.ChromeOptions()
    # option.add_argument("start-maximized")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=option)

    today = datetime.datetime.now()

    driver.get('https://termine.staedteregion-aachen.de/auslaenderamt/?rs')
    driver.find_element(By.ID, "buttonfunktionseinheit-1").click()

    urls = [
        "https://termine.staedteregion-aachen.de/auslaenderamt/location?mdt=78&select_cnc=1&cnc-204=0&cnc-205=0&cnc-198=1&cnc-201=0&cnc-202=0&cnc-227=0&cnc-232=0&cnc-203=0&cnc-196=0&cnc-190=0&cnc-185=0&cnc-187=0&cnc-188=0&cnc-186=0&cnc-192=0&cnc-191=0&cnc-194=0&cnc-197=0&cnc-193=0&cnc-183=0&cnc-184=0&cnc-195=0&cnc-200=0&cnc-228=0",
        "https://termine.staedteregion-aachen.de/auslaenderamt/location?mdt=78&select_cnc=1&cnc-204=0&cnc-205=0&cnc-198=0&cnc-201=1&cnc-202=0&cnc-227=0&cnc-232=0&cnc-203=0&cnc-196=0&cnc-190=0&cnc-185=0&cnc-187=0&cnc-188=0&cnc-186=0&cnc-192=0&cnc-191=0&cnc-194=0&cnc-197=0&cnc-193=0&cnc-183=0&cnc-184=0&cnc-195=0&cnc-200=0&cnc-228=0",
        "https://termine.staedteregion-aachen.de/auslaenderamt/location?mdt=78&select_cnc=1&cnc-204=0&cnc-205=0&cnc-198=0&cnc-201=0&cnc-202=1&cnc-227=0&cnc-232=0&cnc-203=0&cnc-196=0&cnc-190=0&cnc-185=0&cnc-187=0&cnc-188=0&cnc-186=0&cnc-192=0&cnc-191=0&cnc-194=0&cnc-197=0&cnc-193=0&cnc-183=0&cnc-184=0&cnc-195=0&cnc-200=0&cnc-228=0"
    ]

    for i in range(len(urls)):
        driver.get(urls[i])
        driver.find_element(By.CSS_SELECTOR,
                            "input[type='submit'][aria-label='Ausländeramt Aachen, 2. Etage auswählen'][name='select_location'][value='Ausländeramt Aachen, 2. Etage auswählen']").click()

        try:
            driver.find_element(By.XPATH, "//*[contains(text(), 'Kein freier Termin verfügbar')]")
            msg = f"{today}: No appointment available in team: {i + 1}"

        except Exception as e:
            msg = f"{today}: -------------------   Appointment found in team: {i + 1} ----------------"
            elem = driver.find_element(By.XPATH, "//*")
            source_code = elem.get_attribute("outerHTML")
            with open('final_page.html', "w") as file:
                file.write(source_code.encode('utf-8'))

        print(msg)

        with open("logs.txt", "a") as file:
            file.write(msg + "\n")

    driver.close()


Check_appointment()
scheduler = BlockingScheduler()
scheduler.add_job(Check_appointment, 'interval', hours=0.167)
scheduler.start()
