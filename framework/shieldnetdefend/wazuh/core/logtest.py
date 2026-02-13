# Copyright (C) 2015, ShieldnetDefend Inc.
# Created by ShieldnetDefend, Inc. <info@shieldnetdefend.com>.
# This program is a free software; you can redistribute it and/or modify it under the terms of GPLv2

from datetime import datetime

import pytz

from shieldnetdefend.core.common import LOGTEST_SOCKET, DECIMALS_DATE_FORMAT, origin_module
from shieldnetdefend.core.shieldnet_defend_socket import ShieldnetDefendSocketJSON, create_shieldnet_defend_socket_message
from shieldnetdefend.core.exception import ShieldnetDefendError


def send_logtest_msg(command: str = None, parameters: dict = None) -> dict:
    """Connect and send a message to the logtest socket.

    Parameters
    ----------
    command: str
        Command to send to the logtest socket.
    parameters : dict
        Dict of parameters that will be sent to the logtest socket.

    Returns
    -------
    dict
        Response from the logtest socket.
    """
    full_message = create_shieldnet_defend_socket_message(origin={'name': 'Logtest', 'module': origin_module.get()},
                                               command=command,
                                               parameters=parameters)
    logtest_socket = ShieldnetDefendSocketJSON(LOGTEST_SOCKET)
    logtest_socket.send(full_message)
    response = logtest_socket.receive(raw=True)
    logtest_socket.close()
    try:
        response['data']['output']['timestamp'] = datetime.strptime(
            response['data']['output']['timestamp'], "%Y-%m-%dT%H:%M:%S.%f%z").astimezone(pytz.utc).strftime(
            DECIMALS_DATE_FORMAT)
    except KeyError:
        pass

    return response


def validate_dummy_logtest() -> None:
    """Validates a dummy log test by sending a log test message.

    Raises
    ------
    ShieldnetDefendError
        If an error occurs during the log test with error code 1113.
    """
    command = "log_processing"
    parameters = {"location": "dummy", "log_format": "syslog", "event": "Hello"}

    response = send_logtest_msg(command, parameters)
    if response.get('data', {}).get('codemsg', -1) == -1:
        raise ShieldnetDefendError(1113)
