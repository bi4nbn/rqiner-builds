#!/bin/bash

# 定义变量
FILENAME="rqiner-x86-broadwell"
URL="https://github.com/Qubic-Solutions/rqiner-builds/releases/latest/download/$FILENAME"
# 自动获取CPU线程数
THREADS=$(nproc)
ID="KFYHWZGKJDMBGHXLKWLQFPAGXLVCFRMTRDOWZRZBRDMHVBSTRZRIMVWARYSM"
LABEL_AND_SCREEN_NAME="test"

# 优雅地结束FILENAME相关进程和所有SCREEN窗口
pkill -f $FILENAME
screen -ls | awk '/\.Attached/{print $1}' | xargs screen -S -X quit

# 尝试下载，失败后等待5秒再试
until wget -N --quiet --show-progress --no-check-certificate -O "$FILENAME" "$URL"; do
  sleep 5
done

# 修改文件权限以便执行
chmod 755 $FILENAME

# 使用screen执行命令，保障命令在后台运行且在ssh断开后仍然运行
screen -dmS $LABEL_AND_SCREEN_NAME ./$FILENAME -t $THREADS -i $ID -l $LABEL_AND_SCREEN_NAME

echo "脚本运行完毕，$FILENAME 在后台运行中。"