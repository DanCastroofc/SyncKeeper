# Verifica se o caminho do diretorio termina com /
import os
import datetime
import shutil
from . import configModule
from . import logModule

config = configModule.get_conf()

def check_bar (dirValue):
    if isinstance(dirValue, str):
        if not dirValue.endswith('/'):
            dirValue = dirValue + '/'
        return dirValue

def check_dir_exist (dirValue):
    if isinstance(dirValue, str):
        if not os.path.exists(dirValue):
            logModule.report("critical", f"Diretorio não existe. {dirValue}")
            return 1

def check_dir_exist_create (dirValue):
    if isinstance(dirValue, str):
        if not os.path.exists(dirValue):
            os.makedirs(dirValue)
            logModule.report("info", f"Criando diretorio {dirValue}")

def delOldDir(dirDelScan, actualConfig):
    logModule.report('info', 'Verificando Backups Antigos')
    
    nKeepDays = config[actualConfig]["nKeepDays"]
    dataAtual = datetime.datetime.now() # Obtém a data atual
    dataAntiga = dataAtual - datetime.timedelta(days=nKeepDays)
    oldDeleted = False
    
    for diretorioAtual in os.listdir(dirDelScan):
        caminhoCompleto = os.path.join(dirDelScan, diretorioAtual)
        if os.path.isdir(caminhoCompleto):
            dataCriacao = datetime.datetime.fromtimestamp(os.path.getctime(caminhoCompleto))
            if dataCriacao < dataAntiga:
                logModule.report('info', f"Removendo o diretório {caminhoCompleto}")
                shutil.rmtree(caminhoCompleto)
                oldDeleted = True
    
    if not oldDeleted:
        logModule.report('info', f'Não há backups antigos para serem apagados.')

def delOldFile(dirDelScan, actualConfig):
    logModule.report('info', 'Verificando Backups Antigos')
    
    nKeepDays = config[actualConfig]["nKeepDays"]
    dataAtual = datetime.datetime.now() # Obtém a data atual
    dataAntiga = dataAtual - datetime.timedelta(days=nKeepDays)
    oldDeleted = False
    
    for root, dirs, files in os.walk(dirDelScan):
        for file in files:
            caminhoCompleto = os.path.join(root, file)
            dataCriacao = datetime.datetime.fromtimestamp(os.path.getmtime(caminhoCompleto))
            if dataCriacao < dataAntiga:
                logModule.report('info', f"Removendo o arquivo {caminhoCompleto}")
                os.remove(caminhoCompleto)
                oldDeleted = True
    
    if not oldDeleted:
        logModule.report('info', f'Não há backups antigos para serem apagados.')