import shlex
import shutil
import subprocess
import datetime
import os
from . import dirModule
from . import logModule

def backupFiles(originHost, originUser, originDir, destinationDir, diffActive, diffDir, rsyncOptions):
    
    # Checagem de endereços diretorios
    originDir = dirModule.check_bar(originDir)
    destinationDir = dirModule.check_bar(destinationDir)
    
    # Definindo Diretorio Diferencial
    if diffDir and diffActive:
        diffDir = dirModule.check_bar(diffDir)
        diffDirToday = diffDir + str(datetime.date.today()) + "/"
        dirModule.check_dir_exist_create(diffDirToday)
    else:
        diffDirToday = None
    
    # Checagem de Diretorios
    dirModule.check_dir_exist_create(destinationDir)
    
    if dirModule.check_dir_exist(originDir) == 1:
        logModule.report('critical', 'Fatal Error: Origin Directory not found')
        return 1
    
    if not originUser:
        originUser = "root"
    
    # Parametrizando rsync
    rsyncArg = f'rsync {rsyncOptions} '
    
    # Parametrizando host e usuario para rsync
    if originHost == "localhost" or not originHost:
        rsyncArg = f'{rsyncArg} "{originDir}" '
    else:
        rsyncArg = f'{rsyncArg} -o StrictHostKeyChecking=no {originUser}@{originHost}:"{originDir}" '
    
    
    # Parametrizando argumentos do rsync
    rsyncArg = f'{rsyncArg} "{destinationDir}" '
    
    # Checando se o diretorio de diferencial foi definido
    if not diffDir or not diffActive:
        logModule.report('info', 'Differential directory not defined, differential backup will not be performed')
    else:
        rsyncArg = f'{rsyncArg} --backup --backup-dir="{diffDirToday}"'
    
    rsyncArgSplit = shlex.split(rsyncArg)
    
    # Execucao RSync
    logModule.report("info",f'Starting Backup: "{datetime.datetime.now()}"')
    logModule.report("info",f'Host: "{originHost}"')
    logModule.report("info",f'User: "{originUser}"')
    logModule.report("info",f'Origin: "{originDir}"')
    logModule.report("info",f'Destination: "{destinationDir}"')
    logModule.report("info",f'Differential: "{diffDirToday}"')
    logModule.report("info",f'Command: "{rsyncArg}"')
    
    try:
        proc = subprocess.Popen(rsyncArgSplit, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        proc.wait()
    except Exception as e:
        logModule.report('critical', 'Fatal Error: Rsync execution error')
        logModule.report('critical', e)
        return 11
    
    # Verificando codigo de saida
    logModule.report("info",proc.stdout.read().decode())
    
    if proc.returncode != 0:
        logModule.report("critical",proc.stderr.read().decode())
        logModule.report("error",proc.returncode)
        return 1
    else:
        logModule.report("info","Sinchronization completed successfully")
    
    # Apagando pasta diferencial criada se estiver vazia
    
    if diffDir:
        if os.path.exists(diffDirToday) and not os.path.isfile(diffDirToday):
            if not os.listdir(diffDirToday):
                try:
                    os.rmdir(diffDirToday)
                except Exception as e:
                    logModule.report('erro', f'Cannot delete empty differential folder {diffDirToday}')
                    logModule.report('erro', e)
                logModule.report('info', f'No differential backup, deleting empty folder "{diffDirToday}"')
        
        # Apagando Backups antigos
        dirModule.delOldDir(diffDir, "backupFiles")
    
    return 0