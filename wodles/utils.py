# Copyright (C) 2015, ShieldnetDefend Inc.
# Created by ShieldnetDefend, Inc. <info@shieldnetdefend.com>.
# This program is free software; you can redistribute it and/or modify it under the terms of GPLv2

import os
import subprocess
from functools import lru_cache
from sys import exit


@lru_cache(maxsize=None)
def find_shieldnet_defend_path() -> str:
    """
    Get the ShieldnetDefend installation path.

    Returns
    -------
    str
        Path where ShieldnetDefend is installed or empty string if there is no framework in the environment.
    """
    abs_path = os.path.abspath(os.path.dirname(__file__))
    allparts = []
    while 1:
        parts = os.path.split(abs_path)
        if parts[0] == abs_path:  # sentinel for absolute paths
            allparts.insert(0, parts[0])
            break
        elif parts[1] == abs_path:  # sentinel for relative paths
            allparts.insert(0, parts[1])
            break
        else:
            abs_path = parts[0]
            allparts.insert(0, parts[1])

    shieldnet_defend_path = ''
    try:
        for i in range(0, allparts.index('wodles')):
            shieldnet_defend_path = os.path.join(shieldnet_defend_path, allparts[i])
    except ValueError:
        pass

    return shieldnet_defend_path


def call_shieldnet_defend_control(option: str) -> str:
    """
    Execute the shieldnet-defend-control script with the parameters specified.

    Parameters
    ----------
    option : str
        The option that will be passed to the script.

    Returns
    -------
    str
        The output of the call to shieldnet-defend-control.
    """
    shieldnet_defend_control = os.path.join(find_shieldnet_defend_path(), "bin", "shieldnet-defend-control")
    try:
        proc = subprocess.Popen([shieldnet_defend_control, option], stdout=subprocess.PIPE)
        (stdout, stderr) = proc.communicate()
        return stdout.decode()
    except (OSError, ChildProcessError):
        print(f'ERROR: a problem occurred while executing {shieldnet_defend_control}')
        exit(1)


def get_shieldnet_defend_info(field: str) -> str:
    """
    Execute the shieldnet-defend-control script with the 'info' argument, filtering by field if specified.

    Parameters
    ----------
    field : str
        The field of the output that's being requested. Its value can be 'SHIELDNET_DEFEND_VERSION', 'SHIELDNET_DEFEND_REVISION' or
        'SHIELDNET_DEFEND_TYPE'.

    Returns
    -------
    str
        The output of the shieldnet-defend-control script.
    """
    shieldnet_defend_info = call_shieldnet_defend_control("info")
    if not shieldnet_defend_info:
        return "ERROR"

    if not field:
        return shieldnet_defend_info

    env_variables = shieldnet_defend_info.rsplit("\n")
    env_variables.remove("")
    shieldnet_defend_env_vars = dict()
    for env_variable in env_variables:
        key, value = env_variable.split("=")
        shieldnet_defend_env_vars[key] = value.replace("\"", "")

    return shieldnet_defend_env_vars[field]


@lru_cache(maxsize=None)
def get_shieldnet_defend_version() -> str:
    """
    Return the version of ShieldnetDefend installed.

    Returns
    -------
    str
        The version of ShieldnetDefend installed.
    """
    return get_shieldnet_defend_info("SHIELDNET_DEFEND_VERSION")


@lru_cache(maxsize=None)
def get_shieldnet_defend_revision() -> str:
    """
    Return the revision of the ShieldnetDefend instance installed.

    Returns
    -------
    str
        The revision of the ShieldnetDefend instance installed.
    """
    return get_shieldnet_defend_info("SHIELDNET_DEFEND_REVISION")


@lru_cache(maxsize=None)
def get_shieldnet_defend_type() -> str:
    """
    Return the type of ShieldnetDefend instance installed.

    Returns
    -------
    str
        The type of ShieldnetDefend instance installed.
    """
    return get_shieldnet_defend_info("SHIELDNET_DEFEND_TYPE")


ANALYSISD = os.path.join(find_shieldnet_defend_path(), 'queue', 'sockets', 'queue')
# Max size of the event that ANALYSISID can handle
MAX_EVENT_SIZE = 65535
