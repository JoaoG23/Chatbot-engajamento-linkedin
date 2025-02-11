from time import sleep
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def give_like_in_post(post):
    sleep(3)
    like_button = WebDriverWait(post, 20).until(
        EC.element_to_be_clickable((By.XPATH, './/*[@aria-label="Reagir com gostei"]'))
    )
    like_button.click()
    sleep(3)
