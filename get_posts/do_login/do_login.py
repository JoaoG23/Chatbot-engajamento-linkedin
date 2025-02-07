from selenium.webdriver.common.by import By

from time import sleep



def do_login(driver, login_data):
    
    driver.get("https://www.linkedin.com/login/pt?fromSignIn=true&trk=guest_homepage-basic_nav-header-signin")
    email = login_data['email']
    password = login_data['password']
    sleep(2)
    
    # while len(driver.find_elements(By.XPATH, '//*[@id="lightbox-cover"]')) < 1:
    #     sleep(2)
    # print("Login efetuado com sucesso.")
    # sleep(2)
    
    user_input = driver.find_element(By.XPATH, '//*[@id="username"]')
    user_input.send_keys(email)
    sleep(1)
    password_input = driver.find_element(By.XPATH, '//*[@id="password"]')
    password_input.send_keys(password)
    
    sleep(2)
    login_button = driver.find_element(By.XPATH, '//*[@id="organic-div"]/form/div[4]/button')
    login_button.click()
    sleep(1)
    