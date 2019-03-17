from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.select import Select
import sys
import yaml
import getpass
import argparse

config = None

try:
    config = yaml.load( open('config.yaml', 'r') )
except FileNotFoundError:
    print("No config.yaml files found! exiting...")
    config_sample = """
      username: my_username
      password: my_password
      charges:
        -
          credit_card: XXXXX1234
          amount:
              - 0.01
              - 0.02
        -
          credit_card: XXXXX4567
          amount:
              - 0.11
              - 0.12
    """
    sample = yaml.load(config_sample)
    yaml.dump(sample, open('config_sample.yaml', 'w'))
    print("created config_sample.yaml file for reference!")
    sys.exit()

parser = argparse.ArgumentParser()
parser.add_argument('-u', '--username', required=False)
parser.add_argument('-p', '--password', required=False)
parser.add_argument('-f', '--force', action='store_true')
parser.add_argument('-q', '--quiet', action='store_true')
args = parser.parse_args()

delay = 30
username = args.username
password = args.password
shouldPay = args.force
headless = args.quiet

if headless:
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')  # Last I checked this was necessary.
    options.add_argument("disable-infobars")
    options.add_argument("window-size=1400,600");
    driver = webdriver.Chrome(chrome_options=options)
else:
    driver = webdriver.Chrome()

def quit():
    choice = input().lower()
    if choice is "n":
        pass
    else:
        driver.close()
        driver.quit()
    exit()

def wait(id):
    try:
        myElem = WebDriverWait(driver, delay).until(
            EC.presence_of_element_located((By.ID, id)))
        print("Page is ready for:",id)
    except TimeoutException:
        print("Timeout for:",id,"\nyou want to close?")
        quit()

def wait_css(id): #This is good for OR conditions like "#id1, #id2"
    try:
        myElem = WebDriverWait(driver, delay).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, id)))
        print("Page is ready for:",id)
    except TimeoutException:
        print("Timeout for:",id,"\nyou want to close?")
        quit()

def wait_xpath(id):
    try:
        myElem = WebDriverWait(driver, delay).until(
            EC.presence_of_element_located((By.XPATH, id)))
        print("Page is ready for:", id)
    except TimeoutException:
        print("Timeout for:", id, "\nyou want to close?")
        quit()

def wow_pay(amount,card):
    global driver
    driver.get("https://login.wowway.com/BillingCenter_SubmitPayment.aspx")
    wait_css("#ctl00_MainContent_lnkAutoPayChangeLPM, #ctl00_MainContent_imgbLogin")
    elems = driver.find_elements_by_id("ctl00_MainContent_imgbLogin")
    if elems:
        wait('ctl00_MainContent_txtLoginUserName')
        inputElement = driver.find_element_by_id("ctl00_MainContent_txtLoginUserName")
        inputElement.send_keys(username)
        inputElement = driver.find_element_by_id("ctl00_MainContent_txtLoginPassword")
        inputElement.send_keys(password)
        elems = driver.find_elements_by_id("ctl00_MainContent_imgbLogin")
        elems2 = driver.find_elements_by_id("ctl00_MainContentt_imgbLogin")
        inputElement.send_keys(Keys.ENTER)
        wait_xpath("//*[contains(text(),'Invalid username')]|//*[@id = 'ctl00_MainContent_imgbBS3_PayNay']")
        if driver.find_elements(By.ID,"ctl00_MainContent_lblLoginError"):
            print("Login Error with username:",username)
            raise Exception("Login Error")
        else:
            driver.get("https://login.wowway.com/BillingCenter_SubmitPayment.aspx")

    wait("ctl00_MainContent_lnkAutoPayChangeLPM")
    inputElement = driver.find_element_by_id("ctl00_MainContent_lnkAutoPayChangeLPM")
    inputElement.click()
    wait('ctl00_MainContent_btnEntryNextClient')

    select = Select(driver.find_element_by_name('ctl00$MainContent$ddlSelectMethod'))
    select.select_by_visible_text(card)
    wait_xpath('//input[@id="ctl00_MainContent_txtAmountToPay" and not(@disabled)]')

    inputElement = driver.find_element_by_id("ctl00_MainContent_txtAmountToPay")
    inputElement.click()
    inputElement.clear()
    inputElement.send_keys(amount)
    inputElement.send_keys(Keys.ENTER)
    wait('ctl00_MainContent_btnLegalAgree')

    inputElement = driver.find_element_by_id("ctl00_MainContent_btnLegalAgree")
    inputElement.click()
    wait('ctl00_MainContent_btnConfirmPayment')
    if shouldPay:
        inputElement = driver.find_element_by_id("ctl00_MainContent_btnConfirmPayment")
        inputElement.click()
        wait('ctl00_MainContent_btnOk')
    else:
        print("Skipping payment! User -f option if you REALLY want to pay!")
        inputElement = driver.find_element_by_id("ctl00_MainContent_btnModifyPayment")
        inputElement.click()

#MAIN
def main():
    global username
    global password
    try:
        if not username:
            username = config['username']
        if not password:
            password = config['password']
            if not password:
                password = getpass.fallback_getpass("Enter Password:")
        for charge in config['charges']:
            credit_card = charge['credit_card']
            for amount in charge['amount']:
                print("Paying:",amount,credit_card)
                stra = repr(amount)
                wow_pay(stra, credit_card)
        print("Process completed sucessfully")
        driver.close()
        driver.quit()
    except:
        print("Interrupted closing")
        driver.close()
        driver.quit()

main()
