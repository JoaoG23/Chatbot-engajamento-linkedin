import logging
import os
from logging.handlers import RotatingFileHandler

# Configuração do logger
logger = logging.getLogger('Chatbot-engajamento-linkedin')
logger.setLevel(logging.INFO)


log_automation_path = os.path.join(os.getcwd(), 'logs', 'logs.log')

# Configuração do manipulador de rotação de arquivos
handler = RotatingFileHandler(log_automation_path, maxBytes=5*1024*1024, backupCount=3)  # 5MB por arquivo, até 3 backups
handler.setLevel(logging.INFO)

# Formatação das mensagens de log
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)

# Adiciona o manipulador ao logger
logger.addHandler(handler)

def write_to_log(message, type='info'):
    if type == 'error':
       return logger.error(str(message))
    
    return logger.info(str(message))

