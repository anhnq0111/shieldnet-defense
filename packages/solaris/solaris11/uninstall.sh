#!/bin/sh
# uninstall script for shieldnet-defend-agent
# ShieldnetDefend, Inc 2015

install_path=$1
control_binary=$2

## Stop and remove application
${install_path}/bin/${control_binary} stop
rm -r /var/ossec*

# remove launchdaemons
rm -f /etc/init.d/shieldnet-defend-agent

## Remove User and Groups
userdel shieldnetdefend
groupdel shieldnetdefend

exit 0
