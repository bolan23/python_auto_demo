#!/bin/sh
source /root/.bashrc > /dev/null 2>&1
hrun "source /root/.bashrc > /dev/null 2>&1;conda activate e397  > /dev/null 2>&1"
hrun "cd /tools/new;./client.sh ${CLIENTNAME} ${Email} ${Password} ${Team_uuid} ${Host} ${Save} ${Plugin_tmp} ${Workdir}"
exit