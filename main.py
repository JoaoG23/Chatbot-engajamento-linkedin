from time import sleep   
from app import app   

if __name__ == '__main__':
    
    while True:      
        app()
        
        TIME_EVERY_8_HOURS = 28800
        sleep(TIME_EVERY_8_HOURS)