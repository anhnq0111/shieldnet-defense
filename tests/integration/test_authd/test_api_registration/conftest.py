"""
Copyright (C) 2015-2024, ShieldnetDefend Inc.
Created by ShieldnetDefend, Inc. <info@shieldnetdefend.com>.
This program is free software; you can redistribute it and/or modify it under the terms of GPLv2
"""
import pytest

from shieldnet_defend_testing.constants.paths.logs import SHIELDNET_DEFEND_API_LOG_FILE_PATH, SHIELDNET_DEFEND_API_JSON_LOG_FILE_PATH
from shieldnet_defend_testing.utils.callbacks import generate_callback
from shieldnet_defend_testing.tools.monitors import file_monitor
from shieldnet_defend_testing.constants.api import SHIELDNET_DEFEND_API_PORT
from shieldnet_defend_testing.modules.api.patterns import API_STARTED_MSG


@pytest.fixture(scope='module')
def wait_for_api_startup_module():
    """Monitor the API log file to detect whether it has been started or not.

    Raises:
        RuntimeError: When the log was not found.
    """
    # Set the default values
    logs_format = 'plain'
    host = ['0.0.0.0', '::']
    port = SHIELDNET_DEFEND_API_PORT

    # Check if specific values were set or set the defaults
    file_to_monitor = SHIELDNET_DEFEND_API_JSON_LOG_FILE_PATH if logs_format == 'json' else SHIELDNET_DEFEND_API_LOG_FILE_PATH
    monitor_start_message = file_monitor.FileMonitor(file_to_monitor)
    monitor_start_message.start(
        callback=generate_callback(API_STARTED_MSG, {
            'host': str(host),
            'port': str(port)
        })
    )

    if monitor_start_message.callback_result is None:
        raise RuntimeError('The API was not started as expected.')
