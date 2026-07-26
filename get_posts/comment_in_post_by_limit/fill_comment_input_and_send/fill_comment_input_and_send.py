from time import sleep
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from utils.logging.log_manager.log_manager import write_to_log

import os


def validate_in_post_already_commented(post):
    sleep(1)
    elemento = post.find_element(By.CLASS_NAME, 'comments-comment-meta__description-title')
    # elemento = post.find_element(By.XPATH, '//*[@id="ember798"]/div[1]/div[1]/a[2]/h3/span[1]')
    is_commented_by_me =  "João Guilherme" in elemento.text
    if is_commented_by_me:
        write_to_log(f"Post já comentado por mim: {elemento.text}", type='info')
        return True
    return False
    
def validate_if_environment_is_dev():
    is_dev = os.getenv("ENVIRONMENT") == "dev"
    return is_dev

def fill_comment_input_and_send(driver, post, comment_post, quantity_posts_comments):
    try:
        # Clica no botão "Comentar" para abrir a caixa de texto
        comment_button = WebDriverWait(post, 20).until(
            EC.element_to_be_clickable((By.XPATH, './/button[.//span[normalize-space(text())="Comentar"]]'))
        )
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", comment_button)
        sleep(1)
        comment_button.click()
        
        sleep(5)
        # Localiza o input de texto usando aria-label ou data-placeholder dentro do post
        comment_input = WebDriverWait(post, 20).until(
            EC.element_to_be_clickable((By.XPATH, './/*[@aria-label="Editor de texto para criar comentário" or @data-placeholder="Adicionar comentário…"]'))
        )
        comment_input.send_keys(comment_post)
        
        is_post_already_commented = validate_in_post_already_commented(post=post)
        if is_post_already_commented:
            return
        
        is_dev = validate_if_environment_is_dev()
        if is_dev:
            write_to_log(f"Comentário de testes: {comment_post}", type='info')
            return
        
        sleep(3)
        # O botão de enviar o comentário também tem o texto "Comentar", normalmente é o último localizado dentro do post
        send_buttons = WebDriverWait(post, 15).until(
            EC.presence_of_all_elements_located((By.XPATH, './/button[.//span[normalize-space(text())="Comentar"]]'))
        )
        send_buttons[-1].click()

        # # Envia a mensagem usando Ctrl+Enter
        # actions = ActionChains(driver)

        # actions.key_down(Keys.CONTROL).send_keys(Keys.ENTER).key_up(Keys.CONTROL).perform()
        # sleep(3)
                    
        # # Pressiona ESC para fechar qualquer popup
        # actions = ActionChains(driver)
        # actions.send_keys(Keys.ESCAPE).perform()
        sleep(7)
    except Exception as e:
        print(f"Erro ao comentar no post: {e}")
        raise e