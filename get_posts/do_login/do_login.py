from selenium.webdriver.common.by import By

from time import sleep
from utils.logging.log_manager.log_manager import write_to_log


def do_login(driver, login_data):
    
    driver.get("https://www.linkedin.com/login/pt?fromSignIn=true&trk=guest_homepage-basic_nav-header-signin")
    email = login_data['email']
    password = login_data['password']
    sleep(2)
    
    email_input = driver.find_element(By.CSS_SELECTOR, 'input[type="email"]')
    password_input = driver.find_element(By.CSS_SELECTOR, 'input[type="password"]')
    
    email_input.send_keys(email)
    sleep(1)
    password_input.send_keys(password)
    
    sleep(2)
    login_button = driver.find_element(By.XPATH, '//*[@id="organic-div"]/form/div[4]/button')
    login_button.click()
    sleep(20)
    
    write_to_log("Login efetuado com sucesso.", type='info')
    