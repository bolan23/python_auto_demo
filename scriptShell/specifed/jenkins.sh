#!/bin/sh
source /root/.bashrc > /dev/null 2>&1
Plugin_tmp=/tools/new/specified/tmp
Workdir=/data/jenkins/workspace/${JOB_BASE_NAME}
# hrun "cd /tools/new;source /root/.bashrc > /dev/null 2>&1;conda activate e397  > /dev/null 2>&1"
hrun "cd /tools/new;source /root/.bashrc > /dev/null 2>&1;./specifed.sh ${URLS} ${Email} ${Password} ${Team_uuid} ${Host} ${Save} ${Plugin_tmp} ${Workdir}"
exit


用户邮箱:idatest4@ones.ai
用户密码:eCEBg0aFHaaB
测试地址:http://120.78.237.122:10012
测试团队:SNdTDDyE
是否保存:true
插件空间:/tools/new/specified/tmp
工作空间:/data/jenkins/workspace/测试指定插件

用户邮箱:marsdev@ones.ai
用户密码:Test1234
测试地址:http://120.78.74.41
测试团队:MarP5PB7
是否保存:true
插件空间:/tools/new/specified/tmp
工作空间:/data/jenkins/workspace/RunAllPlugs