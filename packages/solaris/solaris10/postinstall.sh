#!/bin/sh
# postinst script for shieldnet-defend-agent
# ShieldnetDefend, Inc 2015

OSSEC_HIDS_TMP_DIR="/tmp/shieldnet-defend-agent"
DIR="/var/ossec"

# Restore the ossec.confs, client.keys and local_internal_options
if [ -f ${OSSEC_HIDS_TMP_DIR}/client.keys ]; then
    cp ${OSSEC_HIDS_TMP_DIR}/client.keys ${DIR}/etc/client.keys
fi
# Restore ossec.conf configuration
if [ -f ${OSSEC_HIDS_TMP_DIR}/ossec.conf ]; then
    mv ${OSSEC_HIDS_TMP_DIR}/ossec.conf ${DIR}/etc/ossec.conf
    chmod 640 ${DIR}/etc/ossec.conf
fi
# Restore client.keys configuration
if [ -f ${OSSEC_HIDS_TMP_DIR}/local_internal_options.conf ]; then
    mv ${OSSEC_HIDS_TMP_DIR}/local_internal_options.conf ${DIR}/etc/local_internal_options.conf
fi

# logrotate configuration file
if [ -d /etc/logrotate.d/ ]; then
    if [ -e /etc/logrotate.d/shieldnet-defend-hids ]; then
        rm -f /etc/logrotate.d/shieldnet-defend-hids
    fi
    cp -p ${DIR}/etc/logrotate.d/shieldnet-defend-hids /etc/logrotate.d/shieldnet-defend-hids
    chmod 644 /etc/logrotate.d/shieldnet-defend-hids
    chown root:root /etc/logrotate.d/shieldnet-defend-hids
    rm -rf ${DIR}/etc/logrotate.d
fi

# Service
if [ -f /etc/init.d/shieldnet-defend-agent ]; then
        /etc/init.d/shieldnet-defend-agent stop > /dev/null 2>&1
fi

## Delete tmp directory
if [ -d ${OSSEC_HIDS_TMP_DIR} ]; then
    rm -r ${OSSEC_HIDS_TMP_DIR}
fi
