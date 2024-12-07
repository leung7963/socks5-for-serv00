#!/bin/bash

USER=$(whoami)
WORKDIR="/home/${USER}/.nezha-agent"
FILE_PATH="/home/${USER}/.s5"
CRON_S5="nohup ${FILE_PATH}/s5 -c ${FILE_PATH}/config.json >/dev/null 2>&1 &"
CRON_NEZHA="nohup ${WORKDIR}/start.sh >/dev/null 2>&1 &"
PM2_PATH="/home/${USER}/.npm-global/lib/node_modules/pm2/bin/pm2"
CRON_JOB="*/12 * * * * $PM2_PATH resurrect >> /home/$(whoami)/pm2_resurrect.log 2>&1"
REBOOT_COMMAND="@reboot pkill -kill -u $(whoami) && $PM2_PATH resurrect >> /home/$(whoami)/pm2_resurrect.log 2>&1"

echo "检查并 重启 任务"


# 检查进程是否在运行

echo "检查php"
pgrep -x "php" > /dev/null


#如果没有运行，则启动 nezha
if [ $? -ne 0 ]; then
    nohup ./vless/start.sh >/dev/null 2>&1 &
    echo "运行成功php"
fi

echo "检查http"
pgrep -x "http" > /dev/null


if [ $? -ne 0 ]; then
    nohup ./vless/http -c ./vless/config.json >/dev/null 2>&1 &
    echo "http运行成功"
fi



# 检查进程是否在运行
echo "检查node"
pgrep -x "node" > /dev/null


if [ $? -ne 0 ]; then
    nohup ./vless/tunnel.sh >/dev/null 2>&1 &
    echo "node运行成功"
fi
