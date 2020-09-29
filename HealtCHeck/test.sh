#!/bin/bash 

function check_variable()
{
if test -z "$1"
then
      echo "$2 DOWN"
else
      echo "$2 UP"
fi
}




lrpC1=`curl -m 10 -sk  https://lrp.in00c1.in.infra/lrp-web | grep -E "302|200"`
merC1=`curl -m 10 -sk  https://mer.in00c1.in.infra/mer-web | grep -E "302|200"`
ntfC1=`curl -m 10 -sk  https://ntf.in00c1.in.infra/notifier | grep -E "302|200"`
stmC1=`curl -m 10 -sk  https://stm.in00c1.in.infra/stm-web | grep -E "302|200"`

check_variable "$lrpC1" "LRP_C1"
check_variable "$merC1" "MER_C1"
check_variable "$ntfC1" "NTF_C1"
check_variable "$stmC1" "STM_C1"
