from time import sleep
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def give_like_in_post(post):
    sleep(3)
    like_button = WebDriverWait(post, 20).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "button.artdeco-button.artdeco-button--muted.artdeco-button--3.artdeco-button--tertiary.ember-view.social-actions-button.react-button__trigger"))
    )
    
    like_button_aria_label_value = like_button.get_attribute('aria-label')
    if like_button_aria_label_value == 'Reagir com gostei':
        like_button.click()
    sleep(3)
