
import os
import traceback

from dotenv import load_dotenv

from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service

from get_posts.do_login.do_login import do_login
from get_posts.search_posts_and_comment.search_posts_and_comment import search_posts_and_comment

from utils.logging.log_manager.log_manager import write_to_log

options = webdriver.ChromeOptions()
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--disable-gpu")
service = Service(ChromeDriverManager().install())

driver = webdriver.Chrome(service=service, options=options)

load_dotenv() 
        
def app():
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
        write_to_log("Aplicação INICIADA! Este um Bot de automação para comentar em posts do LinkedIn.", type='info')

        driver.implicitly_wait(15)
        driver.maximize_window()
        
        user_login = {
            'email': os.getenv("USER_LINKEDIN"),
            'password': os.getenv("PASSWORD_LINKEDIN")
        }
        do_login(driver, user_login)
        
        search_posts_and_comment(driver)
   
    except WebDriverException as e:
        write_to_log(f"WebDriverException: {traceback.format_exc()}", type='error')
    except Exception as e:
        write_to_log(f"Exception: {traceback.format_exc()}", type='error')
    finally:
        print("Encerrando automação")
        write_to_log("Aplicação ENCERRADA!", type='info')
        driver.quit()   