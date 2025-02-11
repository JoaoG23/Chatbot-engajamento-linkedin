from time import sleep

def scroll_by_limit_comments(driver, limit_comments):
    for _ in range(int(limit_comments - 1)):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        sleep(5)