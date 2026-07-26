from time import sleep
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from get_posts.comment_in_post_by_limit.fill_comment_input_and_send.fill_comment_input_and_send import (
    fill_comment_input_and_send,
)
from get_posts.comment_in_post_by_limit.get_content_in_the_post.get_content_in_the_post import (
    get_content_in_the_post,
)
from get_posts.comment_in_post_by_limit.give_like_in_post.give_like_in_post import (
    give_like_in_post,
)
from get_posts.create_comment_based_post.create_comment_based_post import (
    create_comment_based_post,
)

from utils.remove_emojis_text.remove_emojis_text import remove_emojis_text
from utils.remove_linebreak_text.remove_linebreak_text import remove_linebreak_text
from utils.logging.log_manager.log_manager import write_to_log


def comment_in_post_by_limit(driver, limit_comments):
    SCROLL_PAUSE_TIME = 20
    try:
        sleep(4)
        container_post = WebDriverWait(driver, SCROLL_PAUSE_TIME).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, '[data-testid="mainFeed"]')
            )
        )

        posts = WebDriverWait(container_post, SCROLL_PAUSE_TIME).until(
            EC.presence_of_all_elements_located(
                (By.XPATH, './/div[@role="listitem"]')
            )
        )
        # print(teste)

        # posts = WebDriverWait(container_posts[0], SCROLL_PAUSE_TIME).until(
        #     EC.presence_of_all_elements_located((By.CLASS_NAME, 'fie-impression-container'))
        # )
        write_to_log(f"Quantidade de posts encontrados: {len(posts)}", type="info")
        quantity_posts_comments = 0

        is_posts_empty = len(posts) == 0
        if is_posts_empty:
            return "Nenhum post encontrado tente outra busca"

        is_posts_less_than_limit_comments = len(posts) < limit_comments
        if is_posts_less_than_limit_comments:
            limit_comments = len(posts)

        write_to_log(
            f"Quantidade de posts para comentar: {limit_comments}", type="info"
        )

        for i in range(limit_comments):
            try:
                post = posts[i]
                sleep(6)
                give_like_in_post(post)

                content_in_post = get_content_in_the_post(post)
                sleep(10)
                comment_created = create_comment_based_post(content_in_post)
                comment_without_linebreak = remove_linebreak_text(comment_created)
                comment_without_emoji_and_linebreak = remove_emojis_text(
                    comment_without_linebreak
                )

                fill_comment_input_and_send(
                    driver, post, comment_without_emoji_and_linebreak, i
                )

                quantity_posts_comments += 1
                write_to_log(f"Post {i+1} comentado com sucesso!", type="info")
            except Exception as e:
                write_to_log(f"Erro ao comentar no post {i+1}: {str(e)}", type="error")
                continue

        return quantity_posts_comments
    except Exception as e:
        write_to_log(f"Erro ao comentar nos posts: {str(e)}", type="error")
        raise e
