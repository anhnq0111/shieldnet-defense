#!/bin/sh
# uninstall script for shieldnet-defend-agent
# ShieldnetDefend, Inc 2015

control_binary="shieldnet-defend-control"

if [ ! -f /var/ossec/bin/${control_binary} ]; then
  control_binary="ossec-control"
fi

## Stop and remove application
/var/ossec/bin/${control_binary} stop
rm -rf /var/ossec/

# remove launchdaemons
rm -f /etc/init.d/shieldnet-defend-agent
rm -rf /etc/rc2.d/S97shieldnet-defend-agent
rm -rf /etc/rc3.d/S97shieldnet-defend-agent

## Remove User and Groups
userdel shieldnetdefend 2> /dev/null
groupdel shieldnetdefend 2> /dev/null

exit 0
