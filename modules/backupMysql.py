import shlex
import subprocess
import keyring
import datetime
from . import logModule
from . import dirModule

def backupMysql(conName, dbName, ip, pwdName, pwdUnsafeAuth, pwdUser, backupDir, mysqlDumpOptions):
    backupDir = dirModule.check_bar(backupDir)
    dirModule.check_dir_exist_create(backupDir)

    dataToday = datetime.datetime.now().date()
    backupFile = '"' + backupDir + 'backup-MySql-' + conName + '-' + str(dataToday) + '.sql' + '"'
    
    if not pwdUnsafeAuth or pwdUnsafeAuth == '':
        pwd = keyring.get_password(pwdName, pwdUser)
    else:
        pwd = pwdUnsafeAuth
    
    bkpArgs = f'mysqldump {mysqlDumpOptions} -h {ip} -u {pwdUser} -p{pwd} {dbName} > {backupFile}'
    
    logModule.report("info",f'Iniciando backup do banco de dados "{dbName}"')
    logModule.report("info",f'Host: "{ip}"')
    logModule.report("info",f'User: "{pwdUser}"')
    logModule.report("info",f'Backup file: {backupFile}')
    
    try:
        proc = subprocess.Popen(bkpArgs, shell=True)
        proc.wait()
        logModule.report('debug','1029384781892374')
        logModule.report('debug',proc.returncode)
        if proc.returncode == 0:
            logModule.report("info",f'Backup do banco de dados "{dbName}" concluído com sucesso')
        else:
            logModule.report("critical",f'Erro ao executar backup do banco de dados "{dbName}"')
            logModule.report("critical",f'Mysqldump Error code: {proc.returncode}')    
            return 1
    except Exception as e:
        logModule.report("critical",f'Erro ao executar backup do banco de dados "{dbName}"')
        logModule.report("critical",proc.returncode)
        logModule.report("error",e)
        return 1
    
    # Compacta o arquivo de backup
    try:
        logModule.report("info", "Iniciando compactação do backup")
        procZip = f'gzip --force {backupFile}'
        shlex.split(procZip)
        procZip = subprocess.Popen(procZip, shell=True)
        procZip.wait()
        
        if procZip.returncode == 0:
            logModule.report("info", f'Compactação do backup concluída com sucesso')
        else:
            logModule.report("error", f'Erro ao compactar backup')
            logModule.report("error", f'Gzip return code {procZip.returncode}')
            return 1
    except Exception as e:
        logModule.report("error", f'Erro ao compactar backup')
        logModule.report("error", procZip.returncode)
        logModule.report("error", e)
        return 1
    
    # Apagando Backups Antigos
    try:
        dirModule.delOldFile(backupDir, "backupMysql")
    except Exception as e:
        logModule.report("error", f'Erro ao apagar backups antigos')
        logModule.report("error", e)
        return 1
    
    return 0