#!/bin/bash
cd /tools/new
./start.sh

sleep 1


res=$(curl --max-time 600 --connect-timeout 3 --location --request POST 'http://127.0.0.1:9099/upgrade2' \
    --header 'Content-Type: application/json' \
    --data "{ \
    \"urls\":\"${URLS}\", \
    \"email\":\"${Email}\", \
    \"password\":\"${Password}\", \
    \"team_uuid\":\"${Team_uuid}\", \
    \"host\":\"${Host}\", \
    \"upgradeUrls\":\"${UpgradeUrl}\", \
    \"isUpgrade\":${IsUpgrade}, \
    \"installationMode\":\"preinstalled\",\
    \"save\":${Save}\
    }")



echo "res:"$res

logPath=$(echo $res | jq '.[0].logFilePath' |sed 's/\"//g' )

echo "logPath:"$logPath

#输出日志
cat /tools/new/$logPath | while read line
do
    echo $line
done


#删除内容
rm -rf ${WORKSPACE}/tmp

sleep 1

#打印新的测试报告
mv -f /tools/new/upgrade2/tmp ${WORKSPACE}
