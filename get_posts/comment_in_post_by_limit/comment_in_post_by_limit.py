from time import sleep
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from get_posts.create_comment_based_post.create_comment_based_post import create_comment_based_post
from utils.logging.log_manager.log_manager import write_to_log

SCROLL_PAUSE_TIME = 20
def get_content_in_the_post(post):
    try:
        more_content_button = WebDriverWait(post, SCROLL_PAUSE_TIME).until(
            EC.element_to_be_clickable((By.XPATH, f'.//*[contains(text(), "…mais")]'))
        )
        more_content_button.click()
    except:
        pass 
    
    sleep(3)
    text_of_post = WebDriverWait(post, SCROLL_PAUSE_TIME).until(
        EC.visibility_of_element_located((By.CLASS_NAME, 'feed-shared-update-v2__description'))
    )
    return text_of_post.text

def fill_comment_input_and_send(driver, post, content_post, quantity_posts_comments):
    comment_button = WebDriverWait(post, SCROLL_PAUSE_TIME).until(
        EC.element_to_be_clickable((By.XPATH, './/*[@aria-label="Comentar"]'))
    )
    comment_button.click()
    
    sleep(4)
    comment_inputs = WebDriverWait(post, SCROLL_PAUSE_TIME).until(
        EC.presence_of_all_elements_located((By.XPATH, '//*[@aria-placeholder="Adicionar comentário"]'))
    )
    comment_inputs[quantity_posts_comments].send_keys(content_post)
    
    sleep(2)
    send_button = driver.find_element(By.CSS_SELECTOR, '.comments-comment-box__submit-button--cr.artdeco-button.artdeco-button--1.artdeco-button--primary.ember-view')
    sleep(4)
    # send_button.click()
    # screen = WebDriverWait(driver, SCROLL_PAUSE_TIME).until(
    #     EC.element_to_be_clickable((By.XPATH, '/html/body/div[6]/div[3]/div[2]'))
    # )
    screen = driver.find_element(By.XPATH, '/html/body/div[6]/div[3]/div[2]')
    screen.click()
    sleep(2)
    

def comment_in_post_by_limit(driver, limit_comments):
    sleep(4)
    container_posts = WebDriverWait(driver, SCROLL_PAUSE_TIME).until(
        EC.presence_of_all_elements_located((By.CLASS_NAME, 'scaffold-finite-scroll__content'))
    )
    posts = WebDriverWait(container_posts[0], SCROLL_PAUSE_TIME).until(
        EC.presence_of_all_elements_located((By.CLASS_NAME, 'fie-impression-container'))
    )
    

    # Após ele finalizar a inscrição de tres postagens encontrada
    # O sistema volta a procura mais post para comentar
    # Após encontrar ele começa a tentar prencher os posts do inicio novamente
    # E não os encontra emiter uma excessão
    quantity_posts_comments = 0
    
    for i in range(limit_comments): 
        post = posts[i]
        sleep(6)
        content_in_post = get_content_in_the_post(post)
        comment_created = 'Que shoow!'
    
        fill_comment_input_and_send(driver, post, comment_created,i)  
        
        quantity_posts_comments += 1

    return quantity_posts_comments
