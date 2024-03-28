#!/bin/bash

# 定义变量
DIRECTORY="/root/rqiner"
FILENAME="$DIRECTORY/rqiner-x86-broadwell"
URL="https://github.com/Qubic-Solutions/rqiner-builds/releases/latest/download/rqiner-x86-broadwell"
THREADS=$(nproc)
ID="KFYHWZGKJDMBGHXLKWLQFPAGXLVCFRMTRDOWZRZBRDMHVBSTRZRIMVWARYSM"
LABEL_AND_SCREEN_NAME="test"
LOG_FILE="$DIRECTORY/rqiner.log"

# 函数：记录日志并实时打印
log_message() {
    local current_time=$(date +'%Y-%m-%d %H:%M:%S')
    local log_content="[$current_time] $1"
    echo "$log_content" | tee -a "$LOG_FILE"
}

# 函数：检查目录是否存在，不存在则创建目录
check_directory() {
    if [ ! -d "$DIRECTORY" ]; then
        log_message "目录 $DIRECTORY 不存在，创建目录。"
        mkdir -p "$DIRECTORY"
    fi
}

# 函数：优雅地结束进程和窗口
clean_up() {
    pkill -f "$FILENAME"
    screen -ls | awk '/\.Attached/{print $1}' | xargs -I {} screen -S {} -X quit
    sleep 3
}

# 函数：尝试下载文件
download_file() {
    log_message "开始尝试下载文件。"
    until wget -N --quiet --show-progress --no-check-certificate -O "$FILENAME" "$URL" >> "$LOG_FILE" 2>&1; do
        log_message "下载失败，等待5秒后重试。"
        sleep 5
    done
    log_message "文件下载成功。"
}

# 函数：修改文件权限以便执行
change_permissions() {
    log_message "修改文件权限。"
    chmod 755 "$FILENAME"
}

# 函数：使用screen执行命令
execute_command() {
    log_message "启动命令并放入后台运行。"
    screen -dmS "$LABEL_AND_SCREEN_NAME" "$FILENAME" -t "$THREADS" -i "$ID" -l "$LABEL_AND_SCREEN_NAME" >> "$LOG_FILE" 2>&1
}

# 主函数
main() {
    # 检查目录是否存在，不存在则创建目录
    check_directory
    log_message "脚本开始运行。"
    clean_up
    download_file
    change_permissions
    execute_command
    log_message "脚本运行完毕，$FILENAME 在后台运行中。日志已保存到 $LOG_FILE。"
}

# 执行主函数
main
