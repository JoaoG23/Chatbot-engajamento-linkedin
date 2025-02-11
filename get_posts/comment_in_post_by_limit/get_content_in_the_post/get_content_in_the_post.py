from time import sleep

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from utils.remove_linebreak_text.remove_linebreak_text import remove_linebreak_text

def get_content_in_the_post(post):
    try:
        more_content_button = WebDriverWait(post, 20).until(
            EC.element_to_be_clickable((By.XPATH, f'.//*[contains(text(), "…mais")]'))
        )
        more_content_button.click()
    except:
        pass 
    
    sleep(3)
    text_of_post = WebDriverWait(post, 20).until(
        EC.visibility_of_element_located((By.CLASS_NAME, 'feed-shared-update-v2__description'))
    )
    text_without_linebreak = remove_linebreak_text(text_of_post.text)
    return text_without_linebreak
