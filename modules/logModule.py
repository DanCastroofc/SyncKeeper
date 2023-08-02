import logging
import datetime
import os
from . import configModule
from . import dirModule

logFilePath = configModule.get_conf()['log']['dir']

# Checando direrio de log
if not os.path.exists(logFilePath):
    os.makedirs(logFilePath)

logFilePath = dirModule.check_bar(logFilePath)

# Usa o modulo de Log para configurar o destino do log
logFileName = logFilePath + "Backup-" + str(datetime.date.today()) + ".log"

################################ Somente para teste APAGAR NA VERSÃO FINAL
import os
if os.path.exists(logFileName):
    os.unlink(logFileName)
################################

logging.basicConfig(
    format='%(asctime)2s %(levelname)-8s %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S',
    filename=logFileName)

# Redirecinando Log para Terminal
consoleLog = logging.StreamHandler()
consoleLogFormt = logging.Formatter('%(levelname)-8s %(message)s')
consoleLog.setLevel(logging.INFO)
consoleLog.setFormatter(consoleLogFormt)
logging.getLogger('').addHandler(consoleLog)

def report(logLvl, logMsg):
    getattr(logging, logLvl)(logMsg)