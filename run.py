import requests
import subprocess
import time
import logging

# 配置日志记录器
logging.basicConfig(filename='/root/rqiner/run.log', level=logging.INFO, format='%(asctime)s - %(message)s')

# 定义变量
miner_to_find = "test"
url = 'https://pooltemp.qubic.solutions/info?miner=KFYHWZGKJDMBGHXLKWLQFPAGXLVCFRMTRDOWZRZBRDMHVBSTRZRIMVWARYSM&list=true'

# 循环执行
while True:
    try:
        # 发送GET请求
        response = requests.get(url)

        # 检查响应状态码
        if response.status_code == 200:
            # 检查变量是否在返回的内容中（忽略大小写）
            if miner_to_find.lower() in response.content.decode('utf-8').lower():
                print(f"找到'{miner_to_find}'")
                logging.info(f"找到'{miner_to_find}'")
            else:
                print(f"未找到'{miner_to_find}'")
                logging.info(f"未找到'{miner_to_find}'")
                # 执行Shell命令并将输出重定向到/dev/null
                subprocess.Popen(['sh', '/root/rqiner_install_update.sh'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        else:
            print("请求失败，状态码：", response.status_code)
            logging.error(f"请求失败，状态码：{response.status_code}")
            # 如果请求失败，等待60秒后重试
            time.sleep(120)
            continue  # 继续下一次循环

    except Exception as e:
        print("发生异常:", str(e))
        logging.error(f"发生异常: {str(e)}")

    # 等待600秒
    time.sleep(600)
