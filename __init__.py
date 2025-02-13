
import os
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
        print("********************************")
        print("*                              *")
        print("*       BEM-VINDO(A)!          *")
        print("*  Bot Engajamento linkedin    *")
        print("********************************")
        print("")
        print("Este um Bot de automação para comentar em posts do LinkedIn.")
        print("Esperamos que você aproveite!")
        print("e Um beijo na sua bundinha!....😁")
        
        search_information_input = input("Digite o que deseja buscar no LinkedIn:  ")

        driver.implicitly_wait(15)
        driver.maximize_window()
        
        user_login = {
            'email': os.getenv("USER_LINKEDIN"),
            'password': os.getenv("PASSWORD_LINKEDIN")
        }
        do_login(driver, user_login)
        
        search_posts_and_comment(driver, search_information_input)
   
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