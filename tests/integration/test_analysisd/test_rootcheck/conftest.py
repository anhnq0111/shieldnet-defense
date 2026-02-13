# Copyright (C) 2015-2024, ShieldnetDefend Inc.
# Created by ShieldnetDefend, Inc. <info@shieldnetdefend.com>.
# This program is free software; you can redistribute it and/or modify it under the terms of GPLv2

import pytest

from shieldnet_defend_testing.constants.paths.logs import SHIELDNET_DEFEND_LOG_PATH
from shieldnet_defend_testing.modules.modulesd import patterns
from shieldnet_defend_testing.tools.monitors.file_monitor import FileMonitor
from shieldnet_defend_testing.utils import callbacks
from shieldnet_defend_testing.utils.manage_agents import remove_agents
from shieldnet_defend_testing.utils.services import control_service
from shieldnet_defend_testing.tools.simulators.agent_simulator import create_agents


@pytest.fixture()
def wait_for_rootcheck_start():
    # Wait for module rootcheck starts
    shieldnet_defend_log_monitor = FileMonitor(SHIELDNET_DEFEND_LOG_PATH)
    shieldnet_defend_log_monitor.start(callback=callbacks.generate_callback(patterns.MODULESD_STARTED, {
                              'integration': 'rootcheck'
                          }))
    assert (shieldnet_defend_log_monitor.callback_result == None), f'Error invalid configuration event not detected'


@pytest.fixture()
def simulate_agents(request):
    agents = []
    for _ in range(request.getfixturevalue("test_metadata")["agents_number"]):
       agent = create_agents(1, 'localhost')[0]

    yield agents
    # Delete simulated agents
    control_service('start')
    for agent in agents:
        remove_agents(agent.id,'manage_agents')
    control_service('stop')
