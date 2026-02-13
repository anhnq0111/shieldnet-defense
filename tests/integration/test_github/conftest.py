# Copyright (C) 2015-2024, ShieldnetDefend Inc.
# Created by ShieldnetDefend, Inc. <info@shieldnetdefend.com>.
# This program is free software; you can redistribute it and/or modify it under the terms of GPLv2

import pytest

from shieldnet_defend_testing.constants.paths.logs import SHIELDNET_DEFEND_LOG_PATH
from shieldnet_defend_testing.modules.modulesd import patterns
from shieldnet_defend_testing.tools.monitors.file_monitor import FileMonitor
from shieldnet_defend_testing.utils import callbacks


@pytest.fixture()
def wait_for_github_start():
    # Wait for module github starts
    shieldnet_defend_log_monitor = FileMonitor(SHIELDNET_DEFEND_LOG_PATH)
    shieldnet_defend_log_monitor.start(callback=callbacks.generate_callback(patterns.MODULESD_STARTED, {
                              'integration': 'GitHub'
                          }))
    assert (shieldnet_defend_log_monitor.callback_result == None), f'Error invalid configuration event not detected'
