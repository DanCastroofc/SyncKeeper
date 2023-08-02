![Banner](./media/banner.png)

# Script de Backup Automatizado

Este script Python é usado para realizar backups automatizados de arquivos, bancos de dados MySQL e configurações do PFSense com base nas tarefas ativas definidas no arquivo de configuração YAML.

## Visão do Projeto

Este projeto está **atualmente em desenvolvimento** e tem como objetivo fornecer um script de backup automatizado para arquivos, bancos de dados MySQL e configurações do PFSense. O objetivo é tornar o processo de backup mais eficiente e simplificado para os usuários.

### Status Atual

O script já possui funcionalidades básicas implementadas para realizar backups de arquivos e bancos de dados MySQL, além de capturar as configurações do PFSense. No entanto, o projeto ainda está em fase inicial de desenvolvimento e pode conter erros ou melhorias a serem feitas.

### Contribuições e Sugestões

Sua colaboração é bem-vinda! Se você encontrar problemas, tiver sugestões de melhorias ou quiser adicionar novas funcionalidades, fique à vontade para abrir uma [issue](https://github.com/seu-usuario/seu-repositorio/issues) ou enviar um [pull request](https://github.com/seu-usuario/seu-repositorio/pulls). Sinta-se à vontade para discutir ideias, propor alterações ou tirar dúvidas no processo de desenvolvimento.

### Como Contribuir

1. Faça um fork deste repositório.
2. Crie uma branch com o nome da funcionalidade ou correção que você está adicionando (`git checkout -b minha-nova-funcionalidade`).
3. Faça as alterações desejadas no código.
4. Commit suas alterações (`git commit -m 'Adicionando nova funcionalidade'`).
5. Envie suas alterações para o seu fork (`git push origin minha-nova-funcionalidade`).
6. Abra um [pull request](https://github.com/seu-usuario/seu-repositorio/pulls) para este repositório.
7. Aguarde a análise e discussão da sua contribuição.

## Pré-requisitos

- Python 3.x instalado.

## Configuração

O script requer um arquivo YAML de configuração para definir as tarefas de backup e outras configurações relacionadas. O formato do arquivo YAML deve seguir a estrutura exemplificada abaixo:

```yaml
# Exemplo de arquivo de configuração YAML
activeTasks:
  backupFiles: true
  backupMysql: true
  backupPFsense: true

# Definições das tarefas de backup...
```

## Dependências

O script depende de alguns módulos personalizados (definidos no arquivo `modules.py`) e do módulo `yaml`, que é usado para carregar as configurações do arquivo YAML.

## Executando o Script

Para executar o script, siga os passos abaixo:

1. Garanta que todas as dependências estejam instaladas.
2. Crie o arquivo YAML de configuração seguindo o formato descrito acima.
3. Execute o script Python fornecendo o caminho para o arquivo de configuração como argumento:

```
$ python backup_script.py /caminho/para/arquivo_de_configuracao.yaml
```

## Funcionamento do Script

O script funcionará da seguinte maneira:

1. Carregará as configurações do arquivo YAML de acordo com as tarefas ativas.
2. Iniciará as tarefas de backup de arquivos, MySQL e PFSense, conforme definido nas configurações.
3. O progresso e informações sobre o andamento do backup serão registrados em um arquivo de log.

## Estrutura do Arquivo YAML

O arquivo YAML abaixo contém as configurações necessárias para o funcionamento do script de backup automatizado. O script é responsável por realizar backups de arquivos, bancos de dados MySQL e configurações do PFSense, de acordo com as tarefas ativas definidas neste arquivo.

O arquivo YAML está organizado da seguinte forma:

```yaml
activeTasks:
  backupFiles: true
  backupMysql: true
  backupPFsense: true

activeMonitor:
  zbxModule: true
  influxModule: false

backupFiles:
  addrs:
    - destination: "/caminho/para/destino"
      diffActive: false
      host: exemplo.com
      origin: "/caminho/para/origem"
      user: username
      rsyncOptions: "--verbose --recursive --compress --stats"
  nKeepDays: 180

backupMysql:
  addrs:
    - conName: conexao1
      dbName: database1
      ip: 192.168.1.100
      pwdUnsafeAuth: 'senha123'
      pwdName: dbBackup-conexao1
      pwdUser: userbackup
      mysqlDumpOptions: "--column-statistics=0"
  nKeepDays: 1
  backupDir: "/caminho/para/backup/mysql"

backupPFsense:
  addrs:
    destination: "/caminho/para/destino/pfsense"
    ips:
      - 192.168.1.1
    user: admin
  nKeepDays: 1

log:
  dir: "/caminho/para/diretorio/log"

zabbix:
  configFile: "/caminho/para/zabbix_agentd.conf"
```

## Descrição dos Campos

- `activeTasks`: Define as tarefas de backup ativas ou inativas. Se um valor for `true`, a tarefa correspondente será executada; se for `false`, a tarefa será ignorada.
- `activeMonitor`: Configurações para módulos de monitoramento.
- `backupFiles`: Configurações para o backup de arquivos.
  - `addrs`: Lista de endereços de origem e destino dos arquivos a serem copiados.
  - `nKeepDays`: Número de dias para manter os backups de arquivos.
- `backupMysql`: Configurações para o backup de bancos de dados MySQL.
  - `addrs`: Lista de conexões de bancos de dados MySQL a serem copiadas.
  - `nKeepDays`: Número de dias para manter os backups de bancos de dados MySQL.
  - `backupDir`: Diretório de destino para os backups do MySQL.
- `backupPFsense`: Configurações para o backup das configurações do PFSense.
  - `addrs`: Configurações para conexão com o PFSense.
  - `nKeepDays`: Número de dias para manter os backups das configurações do PFSense.
- `log`: Configurações do diretório para os arquivos de log.
- `zabbix`: Configuração do arquivo de configuração do Zabbix.

## Observações

Substitua os valores de exemplo pelos valores reais que correspondem às suas configurações. Lembre-se de ajustar corretamente os caminhos dos diretórios, IPs, nomes de banco de dados, usuários e senhas de acordo com o ambiente em que o script será executado.

## Aviso

Este script é fornecido apenas como exemplo e pode não funcionar sem a implementação completa das funções e módulos referenciados. Certifique-se de adaptar o código para suas necessidades específicas e garantir a correta implementação dos módulos `modules.py` e das funções utilizadas.

```

Lembrando que esta documentação é um ponto de partida e pode ser estendida ou adaptada conforme o desenvolvimento do projeto e a implementação completa das funções e módulos necessários. É importante que a documentação esteja sempre atualizada à medida que o script evolui.