#!/bin/sh

source /root/.bashrc > /dev/null 2>&1
# 开放能力自动化测试 jenkins-job
#job 工作目录
workdir=/data/jenkins/workspace/${JOB_BASE_NAME}

#设置python虚拟环境
command_source="source /root/.bashrc > /dev/null 2>&1;conda activate e397  > /dev/null 2>&1"

# 打印输出内容
command_show1="echo ${Host}"
command_show2="echo ${Email}"
command_show3="echo ${Password}"
command_show4="echo ${Team_uuid}"
command_show5="echo ${IsOrg}"

#卸载falcons和action
command_uninstall="echo Y | pip uninstall falcons > /dev/null 2>&1 ;echo Y | pip uninstall ones_actions > /dev/null 2>&1"

#安装对应的falcons和action
command_install_falcons=""
command_install_actions="pip install --index-url http://119.23.154.208/repository/ones/simple --trusted-host 119.23.154.208 ones_actions > /dev/null 2>&1"

if [ ${IsOrg} = false ]
then
	command_install_falcons="pip install --index-url http://119.23.154.208/repository/ones/simple --trusted-host 119.23.154.208 falcons==1.3.0 > /dev/null 2>&1 "
else
	command_install_falcons="pip install --index-url http://119.23.154.208/repository/ones/simple --trusted-host 119.23.154.208 falcons> /dev/null 2>&1 "
fi

#登录输入的用户信息，获得token等信息
command_login_init="python3 login.py ${Host} ${Email} ${Password} ${Team_uuid};python3 plugin_init.py"

#运行 abilityexec 项目下的用例文件
command_run="pytest -v test/cases --alluredir=tmp/allure --clean-alluredir --disable-warnings"

hrun "cd $workdir;$command_source;$command_uninstall;$command_install_falcons;$command_install_actions;$command_login_init;$command_run"
exit
