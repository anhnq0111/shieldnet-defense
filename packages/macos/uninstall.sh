#!/bin/sh

## Stop and remove application
sudo /Library/Ossec/bin/shieldnet-defend-control stop
sudo /bin/rm -r /Library/Ossec*

# remove launchdaemons
/bin/rm -f /Library/LaunchDaemons/com.shieldnetdefend.agent.plist

## remove StartupItems
/bin/rm -rf /Library/StartupItems/SHIELDNETDEFEND

## Remove User and Groups
/usr/bin/dscl . -delete "/Users/shieldnetdefend"
/usr/bin/dscl . -delete "/Groups/shieldnetdefend"

/usr/sbin/pkgutil --forget com.shieldnetdefend.pkg.shieldnet-defend-agent
/usr/sbin/pkgutil --forget com.shieldnetdefend.pkg.shieldnet-defend-agent-etc

# In case it was installed via Puppet pkgdmg provider

if [ -e /var/db/.puppet_pkgdmg_installed_shieldnet-defend-agent ]; then
    rm -f /var/db/.puppet_pkgdmg_installed_shieldnet-defend-agent
fi

echo
echo "ShieldnetDefend agent correctly removed from the system."
echo

exit 0
