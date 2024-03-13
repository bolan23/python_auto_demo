#!/bin/bash
cd /tools/new
./start.sh
sleep 1
res=$(curl --connect-timeout 3 --location --request POST 'http://127.0.0.1:9099/clients' \
--header 'Content-Type: application/json' \
--data "{ \
	\"urls\":\"${URLS}\", \
    \"email\":\"${Email}\", \
    \"password\":\"${Password}\", \
    \"team_uuid\":\"${Team_uuid}\", \
    \"host\":\"${Host}\", \
    \"clientName\": \"${CLIENTNAME}\", \
    \"save\":${Save} \
}")
logPath=$(echo $res | jq '.[0].logFilePath' |sed 's/\"//g' )
echo "logPath:"$logPath

#输出日志
cat /tools/new/$logPath | while read line
do
    echo $line
done
rm -rf ${WORKSPACE}/tmp
sleep 1
mv -f /tools/new/client/tmp ${WORKSPACE}
