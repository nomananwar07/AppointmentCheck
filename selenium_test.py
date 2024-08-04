import datetime
import time
import ssl
import smtplib
import os
from dotenv import load_dotenv

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


load_dotenv()


def get_env_variable(env_var):
    try:
        return os.environ[env_var]
    except KeyError:
        raise EnvironmentError(
            (
                f"{env_var} not set in .env file.\n"
                "Make sure a .env file exists at root and "
                f"has variable {env_var} set."
            )
        )


receiver_email = get_env_variable("RECEIVER_EMAIL")
sender_email = get_env_variable("SENDER_EMAIL")
password = get_env_variable("SENDER_EMAIL_PASSWD")


def send_email(message, subject="Appointment Found"):

    port = 465  # For SSL
    smtp_server = "smtp.gmail.com"

    message = (
        f"From: {receiver_email}\r\nTo: {sender_email}\r\n"
        f"Subject: {subject}\r\n\r\n{message}"
    )
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message)


def Check_appointment():
    option = webdriver.ChromeOptions()
    # option.add_argument(
    #     "user-data-dir=C:\\Users\\<USER NAME HERE>\\AppData\\Local\\Google\\Chrome\\User Data"  # noqa: E501
    # )  # Path to your chrome profile
    # option.add_argument("start-maximized")
    option.add_argument("--disable-search-engine-choice-screen")
    option.add_argument("--headless")

    chrome_install = ChromeDriverManager().install()
    folder = os.path.dirname(chrome_install)
    chromedriver_path = os.path.join(folder, "chromedriver.exe")

    driver = webdriver.Chrome(
        service=Service(chromedriver_path), options=option
    )

    try:
        today = datetime.datetime.now()

        driver.get("https://termine.staedteregion-aachen.de/auslaenderamt/?rs")
        time.sleep(2)
        driver.find_element(By.ID, "cookie_msg_btn_yes").click()
        time.sleep(2)
        driver.find_element(By.ID, "buttonfunktionseinheit-1").click()
        time.sleep(2)

        urls = [
            "https://termine.staedteregion-aachen.de/auslaenderamt/location?mdt=89&select_cnc=1&cnc-299=0&cnc-300=0&cnc-293=1&cnc-296=0&cnc-297=0&cnc-301=0&cnc-284=0&cnc-298=0&cnc-291=0&cnc-285=0&cnc-282=0&cnc-283=0&cnc-303=0&cnc-281=0&cnc-287=0&cnc-286=0&cnc-289=0&cnc-292=0&cnc-288=0&cnc-279=0&cnc-280=0&cnc-290=0&cnc-295=0&cnc-294=0",  # noqa: E501
            "https://termine.staedteregion-aachen.de/auslaenderamt/location?mdt=89&select_cnc=1&cnc-299=0&cnc-300=0&cnc-293=0&cnc-296=1&cnc-297=0&cnc-301=0&cnc-284=0&cnc-298=0&cnc-291=0&cnc-285=0&cnc-282=0&cnc-283=0&cnc-303=0&cnc-281=0&cnc-287=0&cnc-286=0&cnc-289=0&cnc-292=0&cnc-288=0&cnc-279=0&cnc-280=0&cnc-290=0&cnc-295=0&cnc-294=0",  # noqa: E501
            "https://termine.staedteregion-aachen.de/auslaenderamt/location?mdt=89&select_cnc=1&cnc-299=0&cnc-300=0&cnc-293=0&cnc-296=0&cnc-297=1&cnc-301=0&cnc-284=0&cnc-298=0&cnc-291=0&cnc-285=0&cnc-282=0&cnc-283=0&cnc-303=0&cnc-281=0&cnc-287=0&cnc-286=0&cnc-289=0&cnc-292=0&cnc-288=0&cnc-279=0&cnc-280=0&cnc-290=0&cnc-295=0&cnc-294=0",  # noqa: E501
        ]

        for i in range(len(urls)):
            driver.get(urls[i])
            time.sleep(3)
            ActionChains(driver).scroll_by_amount(0, 500).perform()
            while 1:
                try:
                    driver.find_element(
                        By.CSS_SELECTOR,
                        "input[type='submit'][aria-label='Ausländeramt Aachen, 2. Etage auswählen'][name='select_location'][value='Ausländeramt Aachen, 2. Etage auswählen']",  # noqa: E501
                    ).click()
                    break
                except Exception:
                    time.sleep(5)

            trial = 1
            found = 1
            while trial < 6:
                try:
                    driver.find_element(
                        By.XPATH,
                        "//*[contains(text(), 'Kein freier Termin verfügbar')]",  # noqa: E501
                    )

                    found = 0
                    break
                except Exception:
                    time.sleep(5)
                    trial += 1
            if found == 0:
                msg = f"{today}: No appointment available in url: {i + 1}"
            else:
                msg = (
                    f"{today}: -------------------   Appointment found in url:"
                    f" {i + 1} ----------------"
                )
                email_message = (
                    "Appointment Found on "
                    f"{today.date()} in Url: {i + 1}\n "
                    "https://termine.staedteregion-aachen.de/auslaenderamt/"
                )
                send_email(email_message)
                # driver.save_screenshot(f"{today}.{i}.png");
                with open(f"{today}.{i}.html", "w", encoding="utf-8") as f:
                    f.write(driver.page_source)
                for x in range(20):
                    print("\a")
                    time.sleep(1)

            print(msg)

            with open("logs.txt", "a") as file:
                file.write(msg + "\n")
    finally:
        driver.close()


def test_chrome_browser_driver_match():
    driver = webdriver.Chrome()
    str1 = driver.capabilities["browserVersion"]
    str2 = driver.capabilities["chrome"]["chromedriverVersion"].split(" ")[0]
    print(f"Chrome Browser Version: {str1[0:2]}")
    print(f"Chrome Driver Version: {str2[0:2]}")
    if str1[0:2] != str2[0:2]:
        raise Exception("please download correct chromedriver version")


test_chrome_browser_driver_match()
send_email("This is a test email", subject="Appointment Script Test Email")


INTERVAL_MINUTES = 5

while True:
    Check_appointment()
    time.sleep(INTERVAL_MINUTES * 60)
