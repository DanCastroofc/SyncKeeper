import modules
import yaml

config = modules.get_conf()
activeTasks = config["activeTasks"]
human_readable = yaml.dump(config, default_flow_style=False)

modules.report('info', 'Starting Backup Script')
modules.report('info', f'Active Tasks: {activeTasks}')
modules.report('info', f'Config: \n{human_readable}')

# Backup dos Arquivos
if activeTasks['backupFiles'] == True:
    error_count = 0
    exitCode = 0
    print(len(config["backupFiles"]["addrs"]))
    for i in range(0, len(config["backupFiles"]["addrs"])):
        originHost =        config["backupFiles"]["addrs"][i]['host']
        originUser =        config["backupFiles"]["addrs"][i]['user']
        originDir =         config["backupFiles"]["addrs"][i]['origin']
        destinationDir =    config["backupFiles"]["addrs"][i]['destination']
        diffActive =        config["backupFiles"]["addrs"][i]['diffActive']
        diffDir =           config["backupFiles"]["addrs"][i]['diffActive']
        rsyncOptions =      config["backupFiles"]["addrs"][i]['rsyncOptions']
        
        try:
            exitCode = modules.backupFiles(originHost, originUser, originDir, destinationDir, diffActive, diffDir, rsyncOptions)
            
            if exitCode != 0:
                modules.report('error', f"Task backupFiles failed with error: {exitCode}")
                error_count += 1
        except Exception as e:
            modules.report('error', f"Task backupFiles failed with error: {e}")
            error_count += 1
    if error_count == 0:
        modules.monitorReport(f'backupFiles', 0)
    else:
        modules.monitorReport(f'backupFiles', 1)
else:
    modules.report('info', 'Task backupFiles disabled')
    modules.monitorReport(f'backupFiles', 3)


#Backup do MySQL
if activeTasks['backupMysql'] == True:
    error_count = 0
    exitCode = 0
    for i in range(0, len(config['backupMysql']['addrs'])):
        conName =       config['backupMysql']['addrs'][i]['conName']
        dbName =        config['backupMysql']['addrs'][i]['dbName']
        ip =            config['backupMysql']['addrs'][i]['ip']
        pwdUnsafeAuth =       config['backupMysql']['addrs'][i]['pwdUnsafeAuth']
        pwdName =       config['backupMysql']['addrs'][i]['pwdName']
        pwdUser =       config['backupMysql']['addrs'][i]['pwdUser']
        mysqlDumpOptions =       config['backupMysql']['addrs'][i]['mysqlDumpOptions']
        backupDir =     config['backupMysql']['backupDir']
        
        try:
            exitCode = modules.backupMysql(conName, dbName, ip, pwdName, pwdUnsafeAuth, pwdUser, backupDir, mysqlDumpOptions)
            
            if exitCode != 0:
                modules.report('error', f"Task backupMysql failed with error: {exitCode}")
                error_count += 1
        except Exception as e:
            modules.report('error', f"Task backupMysql failed with error: {e}")
            error_count += 1
        
    if error_count == 0:
        modules.monitorReport(f'backupMysql', 0)
    else:
        modules.monitorReport(f'backupMysql', 1)
else:
    modules.report('info', 'Task backupMysql disabled')
    modules.monitorReport(f'backupMysql', 3)

# Backup do PFSense
if activeTasks['backupPFsense'] == True:
    error_count = 0
    exitCode = 0
    for i in range(0,len(config['backupPFsense']['addrs']['ips'])):
        pfHost =    config["backupPFsense"]["addrs"]["ips"][i]
        destDir =   config["backupPFsense"]["addrs"]["destination"]
        user =      config["backupPFsense"]["addrs"]["user"]
        
        try:
            exitCode = modules.backupPFsense(pfHost, destDir, user)
            
            if exitCode != 0:
                modules.report('error', f"Task backupPFsense failed with error: {exitCode}")
                error_count += 1
        except Exception as e:
            modules.report('error', f"Task backupPFsense failed with error: {e}")
            error_count += 1
        
    if error_count == 0:
        modules.monitorReport(f'backupPFsense', 0)
    else:
        modules.monitorReport(f'backupPFsense', 1)
else:
    modules.report('info', 'Task backupPFsense disabled')
    modules.monitorReport(f'backupPFsense', 3)