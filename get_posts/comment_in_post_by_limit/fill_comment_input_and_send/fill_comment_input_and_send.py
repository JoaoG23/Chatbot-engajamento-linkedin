from time import sleep
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import os
from dotenv import load_dotenv

load_dotenv()

def fill_comment_input_and_send(driver, post, comment_post, quantity_posts_comments):
    try:
        comment_button = WebDriverWait(post, 20).until(
            EC.element_to_be_clickable((By.XPATH, './/*[@aria-label="Comentar"]'))
        )
        comment_button.click()
        
        sleep(5)
        comment_inputs = WebDriverWait(post, 20).until(
            EC.presence_of_all_elements_located((By.XPATH, '//*[@aria-placeholder="Adicionar comentário"]'))
        )
        comment_inputs[quantity_posts_comments].send_keys(comment_post)
        
        is_dev = os.getenv("ENVIRONMENT") == "dev"
        if is_dev:
            write_to_log(f"Comentário de testes: {comment_post}", type='info')
            return
        
        sleep(2)
        send_button = driver.find_element(By.CSS_SELECTOR, '.comments-comment-box__submit-button--cr.artdeco-button.artdeco-button--1.artdeco-button--primary.ember-view')
        send_button.click()
        sleep(7)
    except Exception as e:
        print(f"Erro ao comentar no post: {e}")
        raise e