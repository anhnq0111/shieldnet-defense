#!/bin/sh
# preremove script for shieldnet-defend-agent
# ShieldnetDefend, Inc 2015

control_binary="shieldnet-defend-control"

if [ ! -f /var/ossec/bin/${control_binary} ]; then
  control_binary="ossec-control"
fi

/var/ossec/bin/${control_binary} stop
