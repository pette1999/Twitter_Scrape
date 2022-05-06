from selenium import webdriver
from selenium.webdriver.common.by import By
import pickle
import requests
from bs4 import BeautifulSoup as bs
import time
from os.path import exists
import logging
import helper

options = webdriver.ChromeOptions()
options.add_argument('--disable-blink-features=AutomationControlled')
options.add_argument('user-agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.75 Safari/537.36"')
options.add_argument("--window-size=1920,1080")
options.add_argument('--ignore-certificate-errors')
options.add_argument('--allow-running-insecure-content')
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)
options.add_argument("--headless")
options.add_argument("--incognito")
driver = webdriver.Chrome(options=options)
driver.execute_script(
    "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
  

def login(email=None, password=None, phone=None, timeout=10):
  if exists('./cookies.pkl'):
    cookies = pickle.load(open("cookies.pkl", "rb"))
    driver.get("https://twitter.com/home")
    for cookie in cookies:
      driver.add_cookie(cookie)
    time.sleep(5)
    return
  driver.get("https://twitter.com/i/flow/login")
  time.sleep(5)
  python_button = driver.find_element(By.TAG_NAME, 'input').send_keys(email)
  python_button = driver.find_element(
      By.XPATH, '//*[@id="layers"]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div/div/div/div[6]/div/span/span').click()
  time.sleep(5)
  python_button = driver.find_element(By.TAG_NAME, 'input').send_keys(phone)
  python_button = driver.find_element(By.XPATH, '//*[@id="layers"]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[2]/div/div/div').click()
  time.sleep(5)
  python_button = driver.find_element(By.XPATH, '//*[@id="layers"]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[1]/div/div/div[3]/div/label/div/div[2]/div[1]/input').send_keys(password)
  python_button = driver.find_element(By.XPATH, '//*[@id="layers"]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[2]/div/div[1]/div/div/div').click()
  time.sleep(5)
  
  # save the cookie
  pickle.dump(driver.get_cookies(), open("cookies.pkl", "wb"))

def reply(replyText):
  gotUrls = helper.readCol('./data/tweetUrl.csv', 'url')
  replied = helper.readCol('./data/replied.csv', 'id')
  logging.basicConfig(filename="./data/log.log", level=logging.INFO,
                      format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %H:%M:%S')

  login(driver)
  for i in gotUrls:
    if(i not in replied):
      driver.get(i)
      driver.execute_script("window.scrollTo(0, Math.ceil(document.body.scrollHeight/5));")
      time.sleep(5)
      driver.get_screenshot_as_file("screenshot.png")
      driver.find_element(By.XPATH, '//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div/div/section/div/div/div[1]/div/div[2]/div/div[2]/div[1]/div/div/div/div[2]/div[1]/div/div/div/div/div[1]/div/div/div/div/label/div[1]/div/div/div/div/div[2]/div/div/div/div').send_keys(replyText)
      driver.find_element(By.XPATH, '//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div/div/section/div/div/div[1]/div/div[2]/div/div[2]/div[2]/div/div/div/div[2]/div[3]/div/div/div[2]/div[2]').click()
      helper.writeToFile('./data/replied.csv', [i])
      logging.info('replied to this tweet:' + str(i))
      print('replied to this tweet:' + str(i))
      # for each reply, we wait 1 minute
      time.sleep(60)
  driver.close()
