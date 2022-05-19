# #!/usr/bin/env python
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.common.by import By
import time

def setup():
    print ('Starting the browser...')
    options = ChromeOptions()
    options.add_argument("--headless") 
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--remote-debugging-port=9222")
    options.add_argument("--no-sandbox")
    driver = webdriver.Chrome(options=options,executable_path='/home/devops/myagent/_work/1/s/automatedtesting/selenium/chromedriver')
    print ('Browser started successfully. Navigating to the demo page to login.')
    driver.get('https://www.saucedemo.com/')
    return driver
# Start the browser and login with standard_user
def login (driver, user, password):
    # --uncomment when running in Azure DevOps.
    # options = ChromeOptions()
    # options.add_argument("--headless") 
    # driver = webdriver.Chrome(options=options)
    # options = webdriver.ChromeOptions()
    # options.add_experimental_option("detach", True)
    driver.find_element(By.XPATH,'//input[@id="user-name"]').send_keys(user)
    driver.find_element(By.XPATH,'//input[@id="password"]').send_keys(password)
    driver.find_element(By.XPATH,'//input[@id="login-button"]').click()
    time.sleep(3)
    check_login  = driver.find_element(By.XPATH,'//div[@class="header_secondary_container"]/span').text
    assert "PRODUCTS" in check_login
    print ("Successfully logged in as "+ user)

def add_items_to_cart(driver):
    i = 1
    for element in driver.find_elements(By.XPATH,"//button[text()='Add to cart']"):
        element.click()
        item_name = driver.find_element(By.XPATH,"(//div[@class='inventory_item_name'])["+str(i)+"]").text
        print(item_name + " Added to cart")
        i = i + 1
    number_of_items_in_cart = driver.find_element(By.XPATH,"//span[@class='shopping_cart_badge']").text
    assert "6" in number_of_items_in_cart
    print('All items are successfully added in cart')

def remove_items_from_cart(driver):
    i = 1
    for element in driver.find_elements(By.XPATH,"//button[text()='Remove']"):
        element.click()
        item_name = driver.find_element(By.XPATH,"(//div[@class='inventory_item_name'])["+str(i)+"]").text
        print(item_name + "Removed from cart")
        i = i + 1
    number_of_items_in_cart = driver.find_elements(By.XPATH,"//span[@class='shopping_cart_badge']")
    print (len(number_of_items_in_cart))
    assert len(number_of_items_in_cart)==0
    print('All items are successfully removed from cart')

driver = setup()
login(driver,'standard_user', 'secret_sauce')
add_items_to_cart(driver)
remove_items_from_cart(driver)
driver.quit()
