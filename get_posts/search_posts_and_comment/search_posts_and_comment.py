import os
from time import sleep

from get_posts.comment_in_post_by_limit.comment_in_post_by_limit import comment_in_post_by_limit
from get_posts.encode_message_for_url.encode_message_for_url import encode_message_for_url
from get_posts.scroll_by_limit_comments.scroll_by_limit_comments import scroll_by_limit_comments

from utils.logging.log_manager.log_manager import write_to_log

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

    
def search_posts_and_comment(driver):

    sleep(5)
    driver.get('https://www.linkedin.com/feed/?trk=guest_homepage-basic_nav-header-signin')
    sleep(12)
    
    limit_comments = int(os.getenv("COMMENT_LIMIT"))
    
    scroll_by_limit_comments(driver, limit_comments)
    
    driver.execute_script("window.scrollTo(0, 0);")
    sleep(7)
    
    comment_in_post_by_limit(driver, limit_comments)
        
    mgs = f"Total de comentários: {limit_comments}"
    
    write_to_log(mgs, type='info')
    print(mgs)
    