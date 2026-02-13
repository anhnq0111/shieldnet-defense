# Copyright (C) 2015, ShieldnetDefend Inc.
# Created by ShieldnetDefend, Inc. <info@shieldnetdefend.com>.
# This program is a free software; you can redistribute it and/or modify it under the terms of GPLv2

import os
import sys
from unittest.mock import MagicMock, patch
from shieldnetdefend.core.exception import ShieldnetDefendError


import pytest

sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), '../..'))

with patch('shieldnetdefend.core.common.shieldnet_defend_uid'):
    with patch('shieldnetdefend.core.common.shieldnet_defend_gid'):
        sys.modules['shieldnetdefend.rbac.orm'] = MagicMock()
        import shieldnetdefend.rbac.decorators
        from shieldnetdefend.tests.util import RBAC_bypasser

        del sys.modules['shieldnetdefend.rbac.orm']
        shieldnetdefend.rbac.decorators.expose_resources = RBAC_bypasser

        from shieldnetdefend.event import MSG_HEADER, send_event_to_analysisd


@pytest.mark.parametrize('events,side_effects,message', [
    (['{"foo": 1}'], (None,), 'All events were forwarded to analisysd'),
    (['{"foo": 1}', '{"bar": 2}'], (None, None), 'All events were forwarded to analisysd'),
    (['{"foo": 1}', '{"bar": 2}'], (ShieldnetDefendError(1014), None), 'Some events were forwarded to analisysd'),
    (['{"foo": 1}', '{"bar": 2}'], (ShieldnetDefendError(1014), ShieldnetDefendError(1014)), 'No events were forwarded to analisysd'),
])
@patch('shieldnetdefend.event.ShieldnetDefendAnalysisdQueue.send_msg')
@patch('socket.socket.connect')
def test_send_event_to_analysisd(socket_mock, send_msg_mock, events, side_effects, message):
    send_msg_mock.side_effect = side_effects
    ret_val = send_event_to_analysisd(events=events)

    assert send_msg_mock.call_count == len(events)
    for i, event in enumerate(events):
        assert send_msg_mock.call_args_list[i].kwargs['msg_header'] == MSG_HEADER
        assert send_msg_mock.call_args_list[i].kwargs['msg'] == event

    assert ret_val.affected_items == [events[i] for i, v in enumerate(side_effects) if v is None]
    assert ret_val.message == message
