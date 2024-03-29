import subprocess
from datetime import datetime
import requests
import time

# 定义全局变量
URL = 'https://pooltemp.qubic.solutions/info?miner=KFYHWZGKJDMBGHXLKWLQFPAGXLVCFRMTRDOWZRZBRDMHVBSTRZRIMVWARYSM&list=true'

# 文件路径常量
LOG_FILE_PATH = "/root/rqiner/run.log"
SHELL_SCRIPT_PATH = "/root/rqiner_install_update.sh"
LABEL = ''

def log_message(*args):
    """
    这个函数会在控制台和日志文件同时打印信息，并且在信息前添加时间戳。
    """
    timestamp = datetime.now().strftime("%Y/%m/%d %H:%M:%S")
    message = f"{timestamp} {' '.join(args)}"
    print(message)  # 打印至控制台
    
    with open(LOG_FILE_PATH, "a") as log_file:  # 打印至日志文件
        print(message, file=log_file)

def is_label_exist(label):  # 更具表达性的函数名
    """
    这个函数会检查服务器上是否存在指定的标签
    """
    response = requests.get(URL + label)
    return response.status_code == 200 and label in response.text

def run_shell_script():  # 抽象出运行脚本的函数
    try:
        subprocess.Popen(['bash', SHELL_SCRIPT_PATH])
        log_message("Shell script started successfully.")
        return True
    except Exception as e:
        log_message("Failed to start the shell script:", str(e))
        return False

def get_label_from_script():
    """
    这个函数会从 Shell 脚本中获取 "LABEL_AND_SCREEN_NAME" 的值。
    """
    try:
        with open(SHELL_SCRIPT_PATH, 'r') as script_file:
            for line in script_file:
                if line.startswith('LABEL_AND_SCREEN_NAME='):
                    return line.split('=')[1].strip()
    except Exception as e:
        log_message("Failed to get the label from the shell script:", str(e))
        return None

def main():
    global LABEL
    LABEL = get_label_from_script()  # 从脚本中获取标签

    while LABEL is None:
        log_message("Failed to get the label from the shell script. Trying again...")
        LABEL = get_label_from_script()
        time.sleep(60)  # 如果获取标签失败，则每60秒重试一次

    while True:
        if is_label_exist(LABEL):
            log_message(f"Label '{LABEL}' exists on the server.")
        else:
            log_message(f"Label '{LABEL}' does not exist on the server.")
            log_message("Attempting to run the shell script...")
            run_shell_script()
        time.sleep(60)  # 每60秒检查一次

if __name__ == "__main__":
    main()