#!/bin/sh
# postremove script for shieldnet-defend-agent
# ShieldnetDefend, Inc 2015

if getent passwd shieldnetdefend > /dev/null 2>&1; then
  userdel shieldnetdefend
fi

if getent group shieldnetdefend > /dev/null 2>&1; then
  groupdel shieldnetdefend
fi
