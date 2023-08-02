import yaml
import os

def get_conf():
    # Apontando caminho de um diretorio elatico e paterno
    dir_path =          os.path.dirname(os.path.realpath(__file__))
    parent_dir =        os.path.abspath(os.path.join(dir_path, '..'))
    config_file_path =  os.path.join(parent_dir, 'config.yaml')
    # Lendo o arquivo de configuracao
    with open(config_file_path, "r") as f:
        return yaml.safe_load(f)
    
def write_conf(newConfig):
    # Apontando caminho de um diretorio elatico e paterno
    dir_path =          os.path.dirname(os.path.realpath(__file__))
    parent_dir =        os.path.abspath(os.path.join(dir_path, '..'))
    config_file_path =  os.path.join(parent_dir, 'config.yaml')
    # Lendo o arquivo de configuracao
    with open(config_file_path, "w") as f:
        yaml.dump(newConfig, f, default_flow_style=False)