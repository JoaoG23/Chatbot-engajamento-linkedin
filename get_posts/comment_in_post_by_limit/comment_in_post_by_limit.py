from time import sleep
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from get_posts.comment_in_post_by_limit.fill_comment_input_and_send.fill_comment_input_and_send import fill_comment_input_and_send
from get_posts.comment_in_post_by_limit.get_content_in_the_post.get_content_in_the_post import get_content_in_the_post
from get_posts.comment_in_post_by_limit.give_like_in_post.give_like_in_post import give_like_in_post
from get_posts.create_comment_based_post.create_comment_based_post import create_comment_based_post

from utils.remove_emojis_text.remove_emojis_text import remove_emojis_text
from utils.remove_linebreak_text.remove_linebreak_text import remove_linebreak_text

SCROLL_PAUSE_TIME = 20

def comment_in_post_by_limit(driver, limit_comments):
    sleep(4)
    container_posts = WebDriverWait(driver, SCROLL_PAUSE_TIME).until(
        EC.presence_of_all_elements_located((By.CLASS_NAME, 'scaffold-finite-scroll__content'))
    )
    posts = WebDriverWait(container_posts[0], SCROLL_PAUSE_TIME).until(
        EC.presence_of_all_elements_located((By.CLASS_NAME, 'fie-impression-container'))
    )
    quantity_posts_comments = 0
    
    for i in range(limit_comments): 
        post = posts[i]
        sleep(6)
        give_like_in_post(post)
        
        content_in_post = get_content_in_the_post(post)
        comment_created = create_comment_based_post(content_in_post)
        comment_without_linebreak = remove_linebreak_text(comment_created)
        comment_without_emoji_and_linebreak = remove_emojis_text(comment_without_linebreak)
    
        fill_comment_input_and_send(driver, post, comment_without_emoji_and_linebreak,i)
        
        quantity_posts_comments += 1

    return quantity_posts_comments
