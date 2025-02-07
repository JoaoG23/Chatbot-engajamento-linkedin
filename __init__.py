
import os
from time import sleep
import traceback

from dotenv import load_dotenv

from httpcore import TimeoutException
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.common.exceptions import NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service

from selenium.common.exceptions import InvalidSelectorException

from get_posts.do_login.do_login import do_login
from get_posts.search_posts_and_comment.search_posts_and_comment import search_posts_and_comment

from utils.logging.log_manager.log_manager import write_to_log

options = webdriver.ChromeOptions()
service = Service(ChromeDriverManager().install())

driver = webdriver.Chrome(service=service, options=options)

load_dotenv()

    
if __name__ == '__main__':
    try:
        driver.maximize_window()
        
        user_login = {
            'email': os.getenv("USER_LINKEDIN"),
            'password': os.getenv("PASSWORD_LINKEDIN")
        }
        do_login(driver, user_login)
        search_data_people = {
            'description': os.getenv("DESCRIPTION"),
            'location': os.getenv("LOCATION")
        }
        # sleep(11)
        
        search_posts_and_comment(driver, search_data_people)
   
    except WebDriverException as e:
        write_to_log(f"WebDriverException: {traceback.format_exc()}", type='error')
    except NoSuchElementException as e:
        write_to_log(f"NoSuchElementException: {traceback.format_exc()}", type='error')
    except InvalidSelectorException as e:
        write_to_log(f"InvalidSelectorException: {traceback.format_exc()}", type='error')
    except TimeoutException as e:
        write_to_log(f"TimeoutException: {traceback.format_exc()}", type='error')
    except Exception as e:
        write_to_log(f"Exception: {traceback.format_exc()}", type='error')
    finally:
        print("Encerrando automação")
        driver.quit()   