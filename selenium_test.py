import datetime
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from apscheduler.schedulers.blocking import BlockingScheduler



def Check_appointment():
    option = webdriver.ChromeOptions()
    # option.add_argument("start-maximized")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=option)

    today = datetime.datetime.now()

    driver.get('https://termine.staedteregion-aachen.de/auslaenderamt/?rs')
    time.sleep(2)
    driver.find_element(By.ID, "buttonfunktionseinheit-1").click()
    time.sleep(2)

    urls = [
        "https://termine.staedteregion-aachen.de/auslaenderamt/location?mdt=86&select_cnc=1&cnc-270=0&cnc-271=0&cnc-264=1&cnc-267=0&cnc-268=0&cnc-272=0&cnc-255=0&cnc-269=0&cnc-262=0&cnc-256=0&cnc-251=0&cnc-253=0&cnc-254=0&cnc-274=0&cnc-252=0&cnc-258=0&cnc-257=0&cnc-260=0&cnc-263=0&cnc-259=0&cnc-249=0&cnc-250=0&cnc-261=0&cnc-266=0&cnc-265=0",
        "https://termine.staedteregion-aachen.de/auslaenderamt/location?mdt=86&select_cnc=1&cnc-270=0&cnc-271=0&cnc-264=0&cnc-267=1&cnc-268=0&cnc-272=0&cnc-255=0&cnc-269=0&cnc-262=0&cnc-256=0&cnc-251=0&cnc-253=0&cnc-254=0&cnc-274=0&cnc-252=0&cnc-258=0&cnc-257=0&cnc-260=0&cnc-263=0&cnc-259=0&cnc-249=0&cnc-250=0&cnc-261=0&cnc-266=0&cnc-265=0",
        "https://termine.staedteregion-aachen.de/auslaenderamt/location?mdt=86&select_cnc=1&cnc-270=0&cnc-271=0&cnc-264=0&cnc-267=0&cnc-268=1&cnc-272=0&cnc-255=0&cnc-269=0&cnc-262=0&cnc-256=0&cnc-251=0&cnc-253=0&cnc-254=0&cnc-274=0&cnc-252=0&cnc-258=0&cnc-257=0&cnc-260=0&cnc-263=0&cnc-259=0&cnc-249=0&cnc-250=0&cnc-261=0&cnc-266=0&cnc-265=0"
    ]

    for i in range(len(urls)):
        driver.get(urls[i])
        time.sleep(3)
        ActionChains(driver).scroll_by_amount(0, 500).perform()
        while 1:
            try:
                driver.find_element(By.CSS_SELECTOR,
                            "input[type='submit'][aria-label='Ausländeramt Aachen, 2. Etage auswählen'][name='select_location'][value='Ausländeramt Aachen, 2. Etage auswählen']").click()
                break
            except Exception as e:
                time.sleep(5)

        trial = 1
        found = 1
        while trial < 6:
            try:
                driver.find_element(By.XPATH, "//*[contains(text(), 'Kein freier Termin verfügbar')]")
                found = 0
                break
            except Exception as e:
                time.sleep(5)
                trial += 1
        if found == 0:
            msg = f"{today}: No appointment available in url: {i + 1}"
        else:
            msg = f"{today}: -------------------   Appointment found in url: {i + 1} ----------------"
            # driver.save_screenshot(f"{today}.{i}.png");
            with open(f"{today}.{i}.html", "w", encoding='utf-8') as f:
                f.write(driver.page_source)
            for x in range(20):
                print('\a')
                time.sleep(1)

        print(msg)

        with open("logs.txt", "a") as file:
            file.write(msg + "\n")

    driver.close()


Check_appointment()
scheduler = BlockingScheduler()
scheduler.add_job(Check_appointment, 'interval', minutes=5)
scheduler.start()