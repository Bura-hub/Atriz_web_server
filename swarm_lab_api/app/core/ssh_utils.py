import paramiko
from .raspberry_config import RASPBERRY_PI_CONFIGS

def list_files_on_pi(config, remote_dir):
    """
    Conecta a la Raspberry Pi vía SSH y lista los archivos .py en el directorio remoto.
    
    :param config: Configuración SSH para la Raspberry Pi.
    :param remote_dir: Directorio remoto donde están los scripts.
    :return: Lista de archivos .py en el directorio remoto.
    """
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(config['host'], username=config['username'], password=config['password'])
        
        sftp = ssh.open_sftp()
        files = sftp.listdir(remote_dir)  # Listar archivos en el directorio remoto
        
        # Filtrar solo los archivos con extensión .py
        python_files = [f for f in files if f.endswith('.py')]
        
        sftp.close()
        ssh.close()
        
        return python_files
    except Exception as e:
        return {"error": str(e)}

def list_scripts_in_all_pis(remote_directory):
    """
    Lista los scripts .py disponibles en todas las Raspberry Pi configuradas.
    
    :param remote_directory: Directorio remoto donde se encuentran los scripts.
    :return: Diccionario con los nombres de archivos para cada Raspberry Pi.
    """
    scripts = {}
    for config in RASPBERRY_PI_CONFIGS:
        scripts[config['host']] = list_files_on_pi(config, remote_directory)
    
    return scripts

def execute_script_on_pi(config, script_name, remote_dir):
    """
    Ejecuta el script Python en la Raspberry Pi seleccionada.
    
    :param config: Configuración SSH para la Raspberry Pi.
    :param script_name: Nombre del script Python a ejecutar.
    :param remote_dir: Directorio remoto donde se encuentra el script.
    :return: Salida del script ejecutado.
    """
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(config['host'], username=config['username'], password=config['password'])

        command = f"python3 {remote_dir}/{script_name}"
        stdin, stdout, stderr = ssh.exec_command(command)

        output = stdout.read().decode()
        error = stderr.read().decode()

        ssh.close()
        
        if error:
            return {"status": "error", "details": error}
        return {"status": "success", "output": output}
    except Exception as e:
        return {"status": "error", "details": str(e)}

def execute_script_in_all_pis(script_name, remote_directory):
    """
    Ejecuta el script en todas las Raspberry Pi configuradas.
    
    :param script_name: Nombre del script Python a ejecutar.
    :param remote_directory: Directorio remoto donde se encuentra el script.
    :return: Resultado de la ejecución de cada Raspberry Pi.
    """
    results = {}
    for config in RASPBERRY_PI_CONFIGS:
        results[config['host']] = execute_script_on_pi(config, script_name, remote_directory)
    
    return results

