import os
from time import sleep
from get_posts.comment_in_post.comment_in_post import comment_in_post
from get_posts.encode_message_for_url.encode_message_for_url import encode_message_for_url
from selenium.webdriver.common.by import By

from utils.logging.log_manager.log_manager import write_to_log

    
def search_posts_and_comment(driver, information_people):
    
    description_people = information_people['description']
    
    description_encoded = encode_message_for_url(description_people)
    sleep(5)
    driver.get(f'https://www.linkedin.com/search/results/content/?keywords={description_encoded}')
    sleep(5)
    
    limit_comments = os.getenv("COMMENT_LIMIT")
    quantity_posts_comments = 0
    
    
    while quantity_posts_comments <= int(limit_comments):
        sleep(7)
        quantity_posts_comments += comment_in_post(driver)
        
        # write_to_log(f"conuctos realizados: {quantity_posts_comments}", type='info')
        sleep(2)
        # driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        # sleep(6)
        # next_page_button = driver.find_element(By.XPATH, '//*[@aria-label="Avançar"]')
        # next_page_button.click()
        # sleep(4)
    mgs = f"Total de comentários: {quantity_posts_comments}"
    
    write_to_log(mgs, type='info')
    print(mgs)
    