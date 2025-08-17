from time import sleep
from utils.logging.log_manager.log_manager import write_to_log

def scroll_by_limit_comments(driver, limit_comments):
    for _ in range(int(limit_comments - 1)):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        sleep(7)
    write_to_log(f"Scrolling {limit_comments} vezes.", type='info')