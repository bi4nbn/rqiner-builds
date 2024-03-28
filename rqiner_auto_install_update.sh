#!/bin/bash

# 定义变量
FILENAME="/root/rqiner-x86-broadwell"
URL="https://github.com/Qubic-Solutions/rqiner-builds/releases/latest/download/rqiner-x86-broadwell"
# 自动获取CPU线程数
THREADS=$(nproc)
ID="KFYHWZGKJDMBGHXLKWLQFPAGXLVCFRMTRDOWZRZBRDMHVBSTRZRIMVWARYSM"
LABEL_AND_SCREEN_NAME="test"
LOG_FILE="/root/qb.log"

# 函数：记录日志并实时打印
log_message() {
    local current_time=$(date +'%Y-%m-%d %H:%M:%S')
    local log_content="[$current_time] $1"
    echo "$log_content"
    echo "$log_content" >> "$LOG_FILE"
}

# 记录脚本开始运行的时间
log_message "脚本开始运行。"

# 优雅地结束FILENAME相关进程和所有SCREEN窗口
log_message "结束相关进程和SCREEN窗口。"
pkill -f $FILENAME
screen -ls | awk '/\.Attached/{print $1}' | xargs -I {} screen -S {} -X quit

# 尝试下载，失败后等待5秒再试
log_message "开始尝试下载文件。"
until wget -N --quiet --show-progress --no-check-certificate -O "$FILENAME" "$URL" >> "$LOG_FILE" 2>&1; do
  log_message "下载失败，等待5秒后重试。"
  sleep 5
done
log_message "文件下载成功。"

# 修改文件权限以便执行
log_message "修改文件权限。"
chmod 755 $FILENAME

# 使用screen执行命令，保障命令在后台运行且在ssh断开后仍然运行
log_message "启动命令并放入后台运行。"
screen -dmS $LABEL_AND_SCREEN_NAME $FILENAME -t $THREADS -i $ID -l $LABEL_AND_SCREEN_NAME >> "$LOG_FILE" 2>&1

log_message "脚本运行完毕，$FILENAME 在后台运行中。日志已保存到 $LOG_FILE。"
