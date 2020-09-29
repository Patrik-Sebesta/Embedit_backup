#!/bin/bash
#echo "DATE: "`date +%m-%d-%Y" %T"`
#Function to check if the curl returned expected result or not
function check_variable()
{
if test -z "$1"
then
      echo "$2 DOWN"
else
      echo "$2 UP"
fi
}

domain=pdcph1.ph.prod

#OSB
osb_user=OpenAPI_User
osb_pass='potU9wibliag'

#OSB B2B
osb_b2b_user=osb_user
osb_b2b_pass='JQBz6Ucj'

#BSL
bsl_user=weblogic
bsl_pass='Wotjabsef8'

#PIF
pif_user=osbuser
pif_pass='nihebdiHac2'

#HSIS
hsis_user=hsisuser
hsis_pass='BaykMytjurp2'

#UMC
umc_user=umc_ws_user
umc_pass='LgUF_mvilr0'

#HSOTP
hsotp_user=osbuser
hsotp_pass='nihebdiHac2'

#Blaze
blaze_user=de-admin
blaze_pass='Whytvebjun'

osb=`curl -m 10 -sk -u $osb_user:$osb_pass https://osb.$domain/OpenAPI/ApplicationManagementService/v11/OpenAPIApplicationManagementService_v11?wsdl | grep -o SUCCESS`
check_variable "$osb" "OSB"

osb_b2b=`curl -m 10 -sk -u $osb_b2b_user:$osb_b2b_pass https://b2b.ph.prod/B2BALL_OSB/CommodityManufacturerService/v1/B2BALL_OSBCommodityManufacturerService_v1?wsdl | grep -o VALIDATED`
check_variable "$osb_b2b" "OSB_B2B"

bsl=`curl -m 10 -sk --user $bsl_user:$bsl_pass -H X-Requested-By:MyClient -H Accept:application/json -X GET http://bsl01-$domain:15001/management/tenant-monitoring/applications | python -m json.tool | grep -C1 "hs-application" | grep "STATE_ACTIVE"`

check_variable "$bsl" "BSL"

bsl_jobs=`curl -m 10 -sk --user $bsl_user:$bsl_pass -H X-Requested-By:MyClient -H Accept:application/json -X GET http://bsl01-$domain:15001/management/tenant-monitoring/applications | python -m json.tool | grep -C1 "bsl-jobs" | grep "STATE_ACTIVE"`

check_variable "$bsl_jobs" "BSL-JOBS"

pif=`curl -m 10 -sLk -u $pif_user:$pif_pass https://pif.$domain/party-web/technical-audit | jq '.records.environmentstatus' | grep -oc OK | grep 4`
#pif=`curl -m 10 -Lks -u $pif_user:$pif_pass https://pif.$domain/party-web/api/pif/v1/customer/2333227 | grep -o 'TestingEkoms'`

check_variable "$pif" "PIF"

lap=`curl -m 10 -sk  https://lap.$domain/lap/rest/status/version | grep -Eo '[0-9]*'`

check_variable "$lap" "LAP"

rcm=`curl -m 10 -ks https://rcm.$domain/rcm/health | jq '.status' | grep 'OK'`
check_variable "$rcm" "RCM"

psrv=`curl -m 10 -sk https://psrv.$domain/printserver/actuator/monitoring/health | jq '.status' | grep 'UP'`
check_variable "$psrv" "PSRV"

cab=`curl -m 10 -sk https://cab.$domain/cabinet/actuator/monitoring/health | jq '.status' | grep 'UP'`
check_variable "$cab" "CAB"

homesis=`curl -m 10 -sk -u $hsis_user:$hsis_pass "https://homesis.$domain/homesis/rest/userData.do?code=123" | grep -o '{}'`
check_variable "$homesis" "HOMESIS"

umc=`curl -m 10 -sk https://um.$domain/user-management/actuator/health | grep -o 'UP'`
check_variable "$umc" "UMC"

blaze=`curl -m 10 -sk -u $blaze_user:$blaze_pass "https://de-online8.$domain/online/actuator/prometheus" | grep -o 'system_cpu_count'`
check_variable "$blaze" "Blaze"

sso=`curl -m 10 -sk https://sso.$domain/auth/health | jq '.status' | grep -oc 'UP'`
check_variable "$sso" "SSO"

mss=`curl -m 10 -sk https://mss.$domain/message-server/technical-audit | grep -oc 'startupDate'`
check_variable "$mss" "MSS_CORE"

mspd=`curl -m 10 -sk https://mspd.$domain/mspd/technical-audit| grep -oc 'startupDate'`
check_variable "$mspd" "MSS_PUSH"

shop=`curl -m 10 -ks -w "%{http_code}" -o /dev/null https://shop.homecredit.ph | grep "302"`
check_variable "$shop" "SHOP"
