import shlex
import subprocess
from . import configModule
from . import logModule

configFile = configModule.get_conf()['zabbix']['configFile']

# Le o arquivo de configuração do Zabbix e retorna o valor da chave informada
def zbx_get_config_line(keyWord):
    try:
        with open(configFile) as f:
            lines = f.readlines()
            for line in lines:
                if not line.startswith("#"):
                    if line.find(keyWord) != -1:
                        formatOutputKey = line.split('=',1)[1]
                        if line.find(',') != -1:
                            formatOutputKey = formatOutputKey.split(',',1)[0]
                        formatOutputKey = formatOutputKey.strip()
                        return formatOutputKey
    except Exception as e:
        logModule.report('error', 'Erro ao ler arquivo de configuração do Zabbix')
        logModule.report('error', e)
        print(e)

def zbxReport(zbxKey, zbxValue):
    zbxServer = zbx_get_config_line('ServerActive')
    zbxHost = zbx_get_config_line('Hostname')
    zbxCmdRaw = f'zabbix_sender -z {zbxServer} -s {zbxHost} -k {zbxKey} -o {zbxValue}'
    zbxCmd = shlex.split(zbxCmdRaw)
    try:
        zbxCmd = subprocess.Popen(zbxCmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        zbxCmd.wait(timeout=20)
        logModule.report('info',zbxCmd.stdout.read())
    except Exception as e:
        logModule.report('error', f'Erro ao enviar dados zabbix. Erro: {e}')
        logModule.report('error', f'Comando: {zbxCmdRaw}')