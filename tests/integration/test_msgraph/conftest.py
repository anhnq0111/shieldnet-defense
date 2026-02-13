# Copyright (C) 2015-2024, ShieldnetDefend Inc.
# Created by ShieldnetDefend, Inc. <info@shieldnetdefend.com>.
# This program is free software; you can redistribute it and/or modify it under the terms of GPLv2

import pytest
import subprocess
import os
from pathlib import Path

from shieldnet_defend_testing.constants.paths.logs import SHIELDNET_DEFEND_LOG_PATH
from shieldnet_defend_testing.constants.paths import SHIELDNET_DEFEND_PATH
from shieldnet_defend_testing.modules.modulesd import patterns
from shieldnet_defend_testing.tools.monitors.file_monitor import FileMonitor
from shieldnet_defend_testing.utils import callbacks
from shieldnet_defend_testing.utils.file import remove_file


@pytest.fixture()
def wait_for_msgraph_start():
    # Wait for module ms-graph starts
    shieldnet_defend_log_monitor = FileMonitor(SHIELDNET_DEFEND_LOG_PATH)
    shieldnet_defend_log_monitor.start(callback=callbacks.generate_callback(patterns.MODULESD_STARTED, {
                              'integration': 'ms-graph'
                          }))
    assert (shieldnet_defend_log_monitor.callback_result == None), f'Error invalid configuration event not detected'


@pytest.fixture(scope="session")
def proxy_setup():
    RESPONSES_PATH = Path(Path(__file__).parent, 'test_API', 'data', 'response_samples', 'responses.json')
    m365proxy = subprocess.Popen(["/tmp/m365proxy/m365proxy", "--mocks-file", RESPONSES_PATH])
    # Configurate proxy for ShieldnetDefend (will only work for systemctl start/restart)
    subprocess.run("systemctl set-environment http_proxy=http://localhost:8000", shell=True)
    remove_file(os.path.join(SHIELDNET_DEFEND_PATH, 'var', 'wodles', 'ms-graph-tenant_id-resource_name-resource_relationship'))

    yield

    subprocess.run("systemctl unset-environment http_proxy", shell=True)
    m365proxy.kill()
    m365proxy.wait()
