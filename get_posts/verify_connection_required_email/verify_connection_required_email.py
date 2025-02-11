from time import sleep
from selenium.webdriver.common.by import By

from utils.logging.log_manager.log_manager import write_to_log

def verify_connection_required_email(driver):

    sleep(7)    
    email_inputs = driver.find_elements(By.XPATH, '//input[@name="email"]')
    if len(email_inputs) == 1:
        sleep(4)    
        exit_button = driver.find_element(By.XPATH, '//*[@aria-label="Fechar"]')
        exit_button.click()
        
        msg = "Conexão nao realizada, pois necessita de um email verificado."
        write_to_log(msg, type='info')
        return
    
    sleep(6) 
    no_send_note_button = driver.find_element(By.XPATH, "//*[text()='Enviar sem nota']")
    no_send_note_button.click()
    sleep(6)