import subprocess
from datetime import datetime
import requests
import time

# 定义全局变量
URL = 'https://pooltemp.qubic.solutions/info?miner='

# 文件路径常量
LOG_FILE_PATH = "/root/rqiner/run.log"
SHELL_SCRIPT_PATH = "/root/rqiner_install_update.sh"

def log_message(*args):
    """
    这个函数会在控制台和日志文件同时打印信息，并且在信息前添加时间戳。
    """
    timestamp = datetime.now().strftime("%Y/%m/%d %H:%M:%S")
    message = f"{timestamp} {' '.join(args)}"
    print(message)  # 打印至控制台
    
    with open(LOG_FILE_PATH, "a") as log_file:  # 打印至日志文件
        print(message, file=log_file)

def is_miner_exist(miner_id):
    """
    这个函数会检查服务器上是否存在指定的矿工ID
    """
    response = requests.get(URL + miner_id + '&list=true')
    return response.status_code == 200 and miner_id in response.text

def run_shell_script():
    """
    创建并运行一个在后台工作的自Shell子进程
    """
    try:
        subprocess.Popen(['bash', SHELL_SCRIPT_PATH])
        log_message("Shell script started successfully.")
        return True
    except Exception as e:
        log_message("Failed to start the shell script:", str(e))
        return False

def get_id_from_script():
    """
    这个函数会从 Shell 脚本中获取 "ID=" 的值
    """
    try:
        with open(SHELL_SCRIPT_PATH, 'r') as script_file:
            for line in script_file:
                if line.startswith('ID='):
                    return line.split('=')[1].strip()
    except Exception as e:
        log_message("Failed to get the ID from the Shell script:", str(e))
        return None

def main():
    miner_id = get_id_from_script()

    while miner_id is None:
        log_message("Failed to get the miner ID from the shell script. Trying again...")
        miner_id = get_id_from_script()
        time.sleep(60)

    while True:
        if is_miner_exist(miner_id):
            log_message(f"Miner ID '{miner_id}' exists on the server.")
        else:
            log_message(f"Miner ID '{miner_id}' does not exist on the server.Tempting to run the shell script...")
            run_shell_script()
        time.sleep(60)

if __name__ == "__main__":
    main()