from time import sleep
from selenium.webdriver.common.by import By

# from connect_people.verify_connection_required_email.verify_connection_required_email import verify_connection_required_email


def comment_in_post(driver):
    
    comments_buttons = driver.find_elements(By.XPATH,"//*[text()='Comentar']")
    sleep(4)
    
    for comments_button in comments_buttons:
        comments_button.click()

        sleep(5)
        
        comment_input = driver.find_element(By.XPATH, f'//*[@aria-placeholder="Adicionar comentário"]')
        sleep(2)
        comment_input.send_keys('Que legal!')
        
        sleep(1)
        send_button = driver.find_element(By.CSS_SELECTOR, 
                                          '.comments-comment-box__submit-button--cr.artdeco-button.artdeco-button--1.artdeco-button--primary.ember-view')
        sleep(2)
        send_button.click()
        # verify_connection_required_email(driver)
    return len(comments_buttons)