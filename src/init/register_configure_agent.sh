#!/bin/bash

# Copyright (C) 2015, ShieldnetDefend Inc.
#
# This program is free software; you can redistribute it
# and/or modify it under the terms of the GNU General Public
# License (version 2) as published by the FSF - Free Software
# Foundation.

# Global variables
INSTALLDIR=${1}
CONF_FILE="${INSTALLDIR}/etc/ossec.conf"
TMP_ENROLLMENT="${INSTALLDIR}/tmp/enrollment-configuration"
TMP_SERVER="${INSTALLDIR}/tmp/server-configuration"
SHIELDNET_DEFEND_REGISTRATION_PASSWORD_PATH="etc/authd.pass"
SHIELDNET_DEFEND_MACOS_AGENT_DEPLOYMENT_VARS="/tmp/shieldnet_defend_envs"


# Set default sed alias
sed="sed -ri"
# By default, use gnu sed (gsed).
use_unix_sed="False"

# Special function to use generic sed
unix_sed() {

    sed_expression="$1"
    target_file="$2"
    special_args="$3"

    sed ${special_args} "${sed_expression}" "${target_file}" > "${target_file}.tmp"
    cat "${target_file}.tmp" > "${target_file}"
    rm "${target_file}.tmp"

}

# Update the value of a XML tag inside the ossec.conf
edit_value_tag() {

    file=""

    if [ -z "$3" ]; then
        file="${CONF_FILE}"
    else
        file="${TMP_ENROLLMENT}"
    fi

    if [ -n "$1" ] && [ -n "$2" ]; then
        start_config="$(grep -n "<$1>" "${file}" | cut -d':' -f 1)"
        end_config="$(grep -n "</$1>" "${file}" | cut -d':' -f 1)"
        if [ -z "${start_config}" ] && [ -z "${end_config}" ] && [ "${file}" = "${TMP_ENROLLMENT}" ]; then
            echo "      <$1>$2</$1>" >> "${file}"
        elif [ "${use_unix_sed}" = "False" ] ; then
            ${sed} "s#<$1>.*</$1>#<$1>$2</$1>#g" "${file}"
        else
            unix_sed "s#<$1>.*</$1>#<$1>$2</$1>#g" "${file}"
        fi
    fi
    
    if [ "$?" != "0" ]; then
        echo "$(date '+%Y/%m/%d %H:%M:%S') agent-auth: Error updating $2 with variable $1." >> "${INSTALLDIR}/logs/ossec.log"
    fi

}

delete_blank_lines() {

    file=$1
    if [ "${use_unix_sed}" = "False" ] ; then
        ${sed} '/^$/d' "${file}"
    else
        unix_sed '/^$/d' "${file}"
    fi

}

delete_auto_enrollment_tag() {

    # Delete the configuration tag if its value is empty
    # This will allow using the default value
    if [ "${use_unix_sed}" = "False" ] ; then
        ${sed} "s#.*<$1>.*</$1>.*##g" "${TMP_ENROLLMENT}"
    else
        unix_sed "s#.*<$1>.*</$1>.*##g" "${TMP_ENROLLMENT}"
    fi

    cat -s "${TMP_ENROLLMENT}" > "${TMP_ENROLLMENT}.tmp"
    mv "${TMP_ENROLLMENT}.tmp" "${TMP_ENROLLMENT}"

}

# Change address block of the ossec.conf
add_adress_block() {

    # Remove the server configuration
    if [ "${use_unix_sed}" = "False" ] ; then
        ${sed} "/<server>/,/\/server>/d" "${CONF_FILE}"
    else
        unix_sed "/<server>/,/\/server>/d" "${CONF_FILE}"
    fi

    # Write the client configuration block
    for i in "${!ADDRESSES[@]}";
    do
        {
            echo "    <server>"
            echo "      <address>${ADDRESSES[i]}</address>"
            echo "      <port>1514</port>"
            if [ -n "${PROTOCOLS[i]}" ]; then
                echo "      <protocol>${PROTOCOLS[i]}</protocol>"
            else
                echo "      <protocol>tcp</protocol>"
            fi 
            echo "    </server>"
        } >> "${TMP_SERVER}"
    done

    if [ "${use_unix_sed}" = "False" ] ; then
        ${sed} "/<client>/r ${TMP_SERVER}" "${CONF_FILE}"
    else
        unix_sed "/<client>/r ${TMP_SERVER}" "${CONF_FILE}"
    fi

    rm -f "${TMP_SERVER}"

}

add_parameter () {

    if [ -n "$3" ]; then
        OPTIONS="$1 $2 $3"
    fi
    echo "${OPTIONS}"

}

get_deprecated_vars () {

    if [ -n "${SHIELDNET_DEFEND_MANAGER_IP}" ] && [ -z "${SHIELDNET_DEFEND_MANAGER}" ]; then
        SHIELDNET_DEFEND_MANAGER=${SHIELDNET_DEFEND_MANAGER_IP}
    fi
    if [ -n "${SHIELDNET_DEFEND_AUTHD_SERVER}" ] && [ -z "${SHIELDNET_DEFEND_REGISTRATION_SERVER}" ]; then
        SHIELDNET_DEFEND_REGISTRATION_SERVER=${SHIELDNET_DEFEND_AUTHD_SERVER}
    fi
    if [ -n "${SHIELDNET_DEFEND_AUTHD_PORT}" ] && [ -z "${SHIELDNET_DEFEND_REGISTRATION_PORT}" ]; then
        SHIELDNET_DEFEND_REGISTRATION_PORT=${SHIELDNET_DEFEND_AUTHD_PORT}
    fi
    if [ -n "${SHIELDNET_DEFEND_PASSWORD}" ] && [ -z "${SHIELDNET_DEFEND_REGISTRATION_PASSWORD}" ]; then
        SHIELDNET_DEFEND_REGISTRATION_PASSWORD=${SHIELDNET_DEFEND_PASSWORD}
    fi
    if [ -n "${SHIELDNET_DEFEND_NOTIFY_TIME}" ] && [ -z "${SHIELDNET_DEFEND_KEEP_ALIVE_INTERVAL}" ]; then
        SHIELDNET_DEFEND_KEEP_ALIVE_INTERVAL=${SHIELDNET_DEFEND_NOTIFY_TIME}
    fi
    if [ -n "${SHIELDNET_DEFEND_CERTIFICATE}" ] && [ -z "${SHIELDNET_DEFEND_REGISTRATION_CA}" ]; then
        SHIELDNET_DEFEND_REGISTRATION_CA=${SHIELDNET_DEFEND_CERTIFICATE}
    fi
    if [ -n "${SHIELDNET_DEFEND_PEM}" ] && [ -z "${SHIELDNET_DEFEND_REGISTRATION_CERTIFICATE}" ]; then
        SHIELDNET_DEFEND_REGISTRATION_CERTIFICATE=${SHIELDNET_DEFEND_PEM}
    fi
    if [ -n "${SHIELDNET_DEFEND_KEY}" ] && [ -z "${SHIELDNET_DEFEND_REGISTRATION_KEY}" ]; then
        SHIELDNET_DEFEND_REGISTRATION_KEY=${SHIELDNET_DEFEND_KEY}
    fi
    if [ -n "${SHIELDNET_DEFEND_GROUP}" ] && [ -z "${SHIELDNET_DEFEND_AGENT_GROUP}" ]; then
        SHIELDNET_DEFEND_AGENT_GROUP=${SHIELDNET_DEFEND_GROUP}
    fi

}

set_vars () {

    export SHIELDNET_DEFEND_MANAGER
    export SHIELDNET_DEFEND_MANAGER_PORT
    export SHIELDNET_DEFEND_PROTOCOL
    export SHIELDNET_DEFEND_REGISTRATION_SERVER
    export SHIELDNET_DEFEND_REGISTRATION_PORT
    export SHIELDNET_DEFEND_REGISTRATION_PASSWORD
    export SHIELDNET_DEFEND_KEEP_ALIVE_INTERVAL
    export SHIELDNET_DEFEND_TIME_RECONNECT
    export SHIELDNET_DEFEND_REGISTRATION_CA
    export SHIELDNET_DEFEND_REGISTRATION_CERTIFICATE
    export SHIELDNET_DEFEND_REGISTRATION_KEY
    export SHIELDNET_DEFEND_AGENT_NAME
    export SHIELDNET_DEFEND_AGENT_GROUP
    export ENROLLMENT_DELAY
    # The following variables are yet supported but all of them are deprecated
    export SHIELDNET_DEFEND_MANAGER_IP
    export SHIELDNET_DEFEND_NOTIFY_TIME
    export SHIELDNET_DEFEND_AUTHD_SERVER
    export SHIELDNET_DEFEND_AUTHD_PORT
    export SHIELDNET_DEFEND_PASSWORD
    export SHIELDNET_DEFEND_GROUP
    export SHIELDNET_DEFEND_CERTIFICATE
    export SHIELDNET_DEFEND_KEY
    export SHIELDNET_DEFEND_PEM

    if [ -r "${SHIELDNET_DEFEND_MACOS_AGENT_DEPLOYMENT_VARS}" ]; then
        . ${SHIELDNET_DEFEND_MACOS_AGENT_DEPLOYMENT_VARS}
        rm -rf "${SHIELDNET_DEFEND_MACOS_AGENT_DEPLOYMENT_VARS}"
    fi

}

unset_vars() {

    vars=(SHIELDNET_DEFEND_MANAGER_IP SHIELDNET_DEFEND_PROTOCOL SHIELDNET_DEFEND_MANAGER_PORT SHIELDNET_DEFEND_NOTIFY_TIME \
          SHIELDNET_DEFEND_TIME_RECONNECT SHIELDNET_DEFEND_AUTHD_SERVER SHIELDNET_DEFEND_AUTHD_PORT SHIELDNET_DEFEND_PASSWORD \
          SHIELDNET_DEFEND_AGENT_NAME SHIELDNET_DEFEND_GROUP SHIELDNET_DEFEND_CERTIFICATE SHIELDNET_DEFEND_KEY SHIELDNET_DEFEND_PEM \
          SHIELDNET_DEFEND_MANAGER SHIELDNET_DEFEND_REGISTRATION_SERVER SHIELDNET_DEFEND_REGISTRATION_PORT \
          SHIELDNET_DEFEND_REGISTRATION_PASSWORD SHIELDNET_DEFEND_KEEP_ALIVE_INTERVAL SHIELDNET_DEFEND_REGISTRATION_CA \
          SHIELDNET_DEFEND_REGISTRATION_CERTIFICATE SHIELDNET_DEFEND_REGISTRATION_KEY SHIELDNET_DEFEND_AGENT_GROUP \
          ENROLLMENT_DELAY)

    for var in "${vars[@]}"; do
        unset "${var}"
    done

}

# Function to convert strings to lower version
tolower () {

    echo "$1" | tr '[:upper:]' '[:lower:]'

}


# Add auto-enrollment configuration block
add_auto_enrollment () {

    start_config="$(grep -n "<enrollment>" "${CONF_FILE}" | cut -d':' -f 1)"
    end_config="$(grep -n "</enrollment>" "${CONF_FILE}" | cut -d':' -f 1)"
    if [ -n "${start_config}" ] && [ -n "${end_config}" ]; then
        start_config=$(( start_config + 1 ))
        end_config=$(( end_config - 1 ))
        sed -n "${start_config},${end_config}p" "${INSTALLDIR}/etc/ossec.conf" >> "${TMP_ENROLLMENT}"
    else
        # Write the client configuration block
        {
            echo "    <enrollment>"
            echo "      <enabled>yes</enabled>"
            echo "      <manager_address>MANAGER_IP</manager_address>"
            echo "      <port>1515</port>"
            echo "      <agent_name>agent</agent_name>"
            echo "      <groups>Group1</groups>"
            echo "      <server_ca_path>/path/to/server_ca</server_ca_path>"
            echo "      <agent_certificate_path>/path/to/agent.cert</agent_certificate_path>"
            echo "      <agent_key_path>/path/to/agent.key</agent_key_path>"
            echo "      <authorization_pass_path>/path/to/authd.pass</authorization_pass_path>"
            echo "      <delay_after_enrollment>20</delay_after_enrollment>"
            echo "    </enrollment>" 
        } >> "${TMP_ENROLLMENT}"
    fi

}

# Add the auto_enrollment block to the configuration file
concat_conf() {

    if [ "${use_unix_sed}" = "False" ] ; then
        ${sed} "/<\/crypto_method>/r ${TMP_ENROLLMENT}" "${CONF_FILE}"
    else
        unix_sed "/<\/crypto_method>/r ${TMP_ENROLLMENT}/" "${CONF_FILE}"
    fi

    rm -f "${TMP_ENROLLMENT}"

}

# Set autoenrollment configuration
set_auto_enrollment_tag_value () {

    tag="$1"
    value="$2"

    if [ -n "${value}" ]; then
        edit_value_tag "${tag}" "${value}" "auto_enrollment"
    else
        delete_auto_enrollment_tag "${tag}" "auto_enrollment"
    fi

}

# Main function the script begin here
main () {

    uname_s=$(uname -s)

    # Check what kind of system we are working with
    if [ "${uname_s}" = "Darwin" ]; then
        sed="sed -ire"
        set_vars
    elif [ "${uname_s}" = "AIX" ] || [ "${uname_s}" = "SunOS" ] || [ "${uname_s}" = "HP-UX" ]; then
        use_unix_sed="True"
    fi

    get_deprecated_vars

    if [ -z "${SHIELDNET_DEFEND_MANAGER}" ] && [ -n "${SHIELDNET_DEFEND_PROTOCOL}" ]; then
        PROTOCOLS=( $(tolower "${SHIELDNET_DEFEND_PROTOCOL//,/ }") )
        edit_value_tag "protocol" "${PROTOCOLS[0]}"
    fi

    if [ -n "${SHIELDNET_DEFEND_MANAGER}" ]; then
        if [ ! -f "${INSTALLDIR}/logs/ossec.log" ]; then
            touch -f "${INSTALLDIR}/logs/ossec.log"
            chmod 660 "${INSTALLDIR}/logs/ossec.log"
            chown root:shieldnetdefend "${INSTALLDIR}/logs/ossec.log"
        fi

        # Check if multiples IPs are defined in variable SHIELDNET_DEFEND_MANAGER
        ADDRESSES=( ${SHIELDNET_DEFEND_MANAGER//,/ } ) 
        PROTOCOLS=( $(tolower "${SHIELDNET_DEFEND_PROTOCOL//,/ }") )
        # Get uniques values if all protocols are the same
        if ( [ "${#PROTOCOLS[@]}" -ge "${#ADDRESSES[@]}" ] && ( ( ! echo "${PROTOCOLS[@]}" | grep -q -w "tcp" ) || ( ! echo "${PROTOCOLS[@]}" | grep -q -w "udp" ) ) ) || [ ${#PROTOCOLS[@]} -eq 0 ] || ( ! echo "${PROTOCOLS[@]}" | grep -q -w "udp" ) ; then
            ADDRESSES=( $(echo "${ADDRESSES[@]}" |  tr ' ' '\n' | cat -n | sort -uk2 | sort -n | cut -f2- | tr '\n' ' ') ) 
        fi
        
        add_adress_block
    fi

    edit_value_tag "port" "${SHIELDNET_DEFEND_MANAGER_PORT}"

    if [ -n "${SHIELDNET_DEFEND_REGISTRATION_SERVER}" ] || [ -n "${SHIELDNET_DEFEND_REGISTRATION_PORT}" ] || [ -n "${SHIELDNET_DEFEND_REGISTRATION_CA}" ] || [ -n "${SHIELDNET_DEFEND_REGISTRATION_CERTIFICATE}" ] || [ -n "${SHIELDNET_DEFEND_REGISTRATION_KEY}" ] || [ -n "${SHIELDNET_DEFEND_AGENT_NAME}" ] || [ -n "${SHIELDNET_DEFEND_AGENT_GROUP}" ] || [ -n "${ENROLLMENT_DELAY}" ] || [ -n "${SHIELDNET_DEFEND_REGISTRATION_PASSWORD}" ]; then
        add_auto_enrollment
        set_auto_enrollment_tag_value "manager_address" "${SHIELDNET_DEFEND_REGISTRATION_SERVER}"
        set_auto_enrollment_tag_value "port" "${SHIELDNET_DEFEND_REGISTRATION_PORT}"
        set_auto_enrollment_tag_value "server_ca_path" "${SHIELDNET_DEFEND_REGISTRATION_CA}"
        set_auto_enrollment_tag_value "agent_certificate_path" "${SHIELDNET_DEFEND_REGISTRATION_CERTIFICATE}"
        set_auto_enrollment_tag_value "agent_key_path" "${SHIELDNET_DEFEND_REGISTRATION_KEY}"
        set_auto_enrollment_tag_value "authorization_pass_path" "${SHIELDNET_DEFEND_REGISTRATION_PASSWORD_PATH}"
        set_auto_enrollment_tag_value "agent_name" "${SHIELDNET_DEFEND_AGENT_NAME}"
        set_auto_enrollment_tag_value "groups" "${SHIELDNET_DEFEND_AGENT_GROUP}"
        set_auto_enrollment_tag_value "delay_after_enrollment" "${ENROLLMENT_DELAY}"
        delete_blank_lines "${TMP_ENROLLMENT}"
        concat_conf
    fi

            
    if [ -n "${SHIELDNET_DEFEND_REGISTRATION_PASSWORD}" ]; then
        echo "${SHIELDNET_DEFEND_REGISTRATION_PASSWORD}" > "${INSTALLDIR}/${SHIELDNET_DEFEND_REGISTRATION_PASSWORD_PATH}"
        chmod 640 "${INSTALLDIR}"/"${SHIELDNET_DEFEND_REGISTRATION_PASSWORD_PATH}"
        chown root:shieldnetdefend "${INSTALLDIR}"/"${SHIELDNET_DEFEND_REGISTRATION_PASSWORD_PATH}"
    fi

    # Options to be modified in ossec.conf
    edit_value_tag "notify_time" "${SHIELDNET_DEFEND_KEEP_ALIVE_INTERVAL}"
    edit_value_tag "time-reconnect" "${SHIELDNET_DEFEND_TIME_RECONNECT}"

    unset_vars

}

# Start script execution
main "$@"
