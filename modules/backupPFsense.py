import shlex
import socket
import subprocess
import datetime
import os
from . import logModule
from . import dirModule

def backupPFsense (pfHost, destDir, user):
    logModule.report('info', 'Iniciando Backup do XML do PFSense')
    
    todayDate = datetime.datetime.now().strftime('%Y-%m-%d')    
    filePath  = "/conf/config.xml"
    destDir = dirModule.check_bar(destDir)
    
    dirModule.check_dir_exist_create(destDir)
    logModule.report('info', f'Diretorio de destino: "{destDir}"')
    
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    result = sock.connect_ex((pfHost,22))
    sock.close()
    if result == 0:      
        logModule.report('info', f'Efetuando Backup do arquivo de configuração XML do host {pfHost}')
        
        destHostDir = f'{destDir}{pfHost}/'
        dirModule.check_dir_exist_create(destHostDir)
        
        # scpArgs = 'scp ' + user + '@' + pfHost + ':"' + filePath + '"' + ' ' + '"' + destHostDir + '"'
        scpArgs = f'scp -o StrictHostKeyChecking=no {user}@{pfHost}:"{filePath}" "{destHostDir}{pfHost}-conf-{todayDate}.xml"'
        scpArgs = shlex.split(scpArgs)
        try:
            proc = subprocess.Popen(scpArgs, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            proc.wait()
            logModule.report("info",proc.stdout.read().decode())
        except Exception as e:
            logModule.report("critical", 'Falha ao executar comando SCP')
            logModule.report("error",e)
            return 1
        
        # Verificando codigo de saida
        if proc.returncode != 0:
            logModule.report("critical",proc.stderr.read().decode())
            logModule.report("error",proc.returncode)
            return 1
        else:
            logModule.report("info","Sincronização concluida!")
    else:
        logModule.report("warning", f'Sem comunicação com host {pfHost} na porta 22. Pulando para o proximo host.')
        return 1
    
    # Apagando Backups Antigos
    try:
        dirModule.delOldFile(destDir, "backupPFsense")
    except Exception as e:
        logModule.report("error", f'Erro ao apagar backups antigos')
        logModule.report("error", e)
        return 1
    return 0