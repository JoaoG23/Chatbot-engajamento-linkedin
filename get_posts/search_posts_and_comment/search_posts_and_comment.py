import os
from time import sleep

from get_posts.comment_in_post_by_limit.comment_in_post_by_limit import comment_in_post_by_limit
from get_posts.scroll_by_limit_comments.scroll_by_limit_comments import scroll_by_limit_comments
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from utils.logging.log_manager.log_manager import write_to_log

def search_posts_and_comment(driver):

    sleep(5)
    driver.get('https://www.linkedin.com/feed/?trk=guest_homepage-basic_nav-header-signin')
    sleep(12)
    
    limit_comments = int(os.getenv("COMMENT_LIMIT"))
    
    scroll_by_limit_comments(driver, limit_comments)
    
    sleep(7)
    
    comment_in_post_by_limit(driver, limit_comments)
        
    mgs = f"Total de comentários: {limit_comments}"
    
    write_to_log(mgs, type='info')
    print(mgs)
    