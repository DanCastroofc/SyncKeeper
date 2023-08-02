import random
import string
import keyring
from getpass import getpass
from . import configModule

def setDBdata():
    conf = configModule.get_conf()

    # Removendo entradas vazias
    for entry in conf['backupMysql']['addrs']:
        if entry['conName'] == '' or entry['conName'] == None:
            conf['backupMysql']['addrs'].remove(entry)
    configModule.write_conf(conf)

    # Coletando dados
    conNameNew = input('Digite o nome da conexão: ')
    ipNew = input('Digite o IP do banco de dados: ')
    dbNameNew = input('Digite o nome do banco de dados: ')
    pwdUserNew = input('Digite o nome do usuário do banco de dados: ')
    pwdNew = getpass('Digite a senha do usuário do banco de dados: ')
    
    # Gerando nome da senha
    pwdNameNew = 'dbBackup-' + conNameNew + '-' + ''.join(random.choices(string.ascii_lowercase, k=8))
    
    # Verificando se a entrada já existe
    entryExists = False
    for entry in conf['backupMysql']['addrs']:
        if entry['conName'] == conNameNew:
            entryExists = True
            
            print('Essa entrada já existe')
            answer = input('Deseja atualizar? (s/n)')
            
            if answer.lower() in ["y","yes","s","sim"]:
                #Apagando senha antiga
                try:
                    keyring.delete_password(entry['pwdName'], entry['pwdUser'])
                except:
                    print("Senha antiga não encontrada, criando nova senha")
                
                #Atualizando dados
                entry['ip'] = ipNew
                entry['dbName'] = dbNameNew
                entry['pwdName'] = pwdNameNew
                entry['pwdUser'] = pwdUserNew
                
                #Criando nova senha
                keyring.set_password(pwdNameNew, pwdUserNew, pwdNew)
                
                #Salvando alterações
                configModule.write_conf(conf)
            elif answer.lower() in ["n","no","nao","não"]:
                print("Finalizando")
            else:
                print("Digite uma resposta válida")
    
    # Se a entrada não existe, cria uma nova  
    if not entryExists:
        keyring.set_password(pwdNameNew, pwdUserNew, pwdNew)
        conf['backupMysql']['addrs'].append({'conName': conNameNew, 'dbName': dbNameNew, 'ip': ipNew, 'pwdName': pwdNameNew, 'pwdUser': pwdUserNew})
        configModule.write_conf(conf)