#!/bin/bash
CLIENTNAME=$1
Email=$2
Password=$3
Team_uuid=$4
Host=$5
Save=$6
Plugin_tmp=$7
Workdir=$8
Plugin_spcace=/tools/new

echo "客户名称:"$CLIENTNAME
echo "用户邮箱:"$Email
echo "用户密码:"$Password
echo "测试地址:"$Host
echo "测试团队:"$Team_uuid
echo "是否保存:"$Save
echo "插件空间:"$Plugin_tmp
echo "工作空间:"$Workdir

# 切换到测试空间的宿主机目录下
cd $Plugin_spcace
source /root/.bashrc > /dev/null 2>&1
conda activate e397  > /dev/null 2>&1
# 检测是否重启web服务
./start.sh

pip install --upgrade pip
echo Y | pip uninstall falcons
echo Y | pip uninstall ones_actions


if [ ${IsOrg} = false ]
then
	pip install --index-url http://119.23.154.208/repository/ones/simple --trusted-host 119.23.154.208 falcons==1.3.0
else
	pip install --index-url http://119.23.154.208/repository/ones/simple --trusted-host 119.23.154.208 falcons
fi
pip install --index-url http://119.23.154.208/repository/ones/simple --trusted-host 119.23.154.208 ones_actions

res=$(curl --max-time 600 --connect-timeout 3 --location --request POST 'http://127.0.0.1:9099/clients' \
--header 'Content-Type: application/json' \
--data "{ \
	  \"clientName\":\"${CLIENTNAME}\", \
    \"email\":\"${Email}\", \
    \"password\":\"${Password}\", \
    \"team_uuid\":\"${Team_uuid}\", \
    \"host\":\"${Host}\", \
    \"save\":${Save} \
}")

logPath=$(echo $res | jq '.[0].logFilePath' |sed 's/\"//g' )


# 输出报告
if [ -z "$logPath" ]
then
	echo "测试用例日志、报告输出失败!!!"
else
  # 输出日志
  cat /tools/new/$logPath | while read line
  do
      echo $line
  done
  sleep 1
  # 输出报告
	rm -rf $Workdir/tmp
	sleep 1
	mv -f $Plugin_tmp $Workdir
fi