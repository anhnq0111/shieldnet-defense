# Copyright (C) 2015-2024, ShieldnetDefend Inc.
# Created by ShieldnetDefend, Inc. <info@shieldnetdefend.com>.
# This program is free software; you can redistribute it and/or modify it under the terms of GPLv2

import pytest

from shieldnet_defend_testing.modules.analysisd.patterns import LOGTEST_STARTED
from shieldnet_defend_testing.tools.monitors.file_monitor import FileMonitor
from shieldnet_defend_testing.utils.callbacks import generate_callback
from shieldnet_defend_testing.constants.paths.logs import SHIELDNET_DEFEND_LOG_PATH

@pytest.fixture(scope='module')
def wait_for_logtest_startup(request):
    """Wait until logtest has begun."""
    log_monitor = FileMonitor(SHIELDNET_DEFEND_LOG_PATH)
    log_monitor.start(callback=generate_callback(LOGTEST_STARTED), timeout=40, only_new_events=True)
