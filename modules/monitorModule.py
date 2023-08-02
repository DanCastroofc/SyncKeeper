from . import configModule
from . import zbxModule
from . import logModule

def monitorReport(monitorKey, monitorValue):
    activeMonitor = configModule.get_conf()['activeMonitor']
    for task, actv in activeMonitor.items():
        if actv == True and task == 'zbxModule':
            logModule.report('info','Sending Zabbix Data')
            zbxModule.zbxReport(monitorKey, monitorValue)