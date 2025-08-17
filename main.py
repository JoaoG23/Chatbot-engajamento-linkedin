from time import sleep   
from app import app   

if __name__ == '__main__':
    
    while True:      
        app()
        
        TIME_EVERY_4_HOURS = 18000
        sleep(TIME_EVERY_4_HOURS)