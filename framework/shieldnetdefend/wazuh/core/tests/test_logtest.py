# Copyright (C) 2015, ShieldnetDefend Inc.
# Created by ShieldnetDefend, Inc. <info@shieldnetdefend.com>.
# This program is free software; you can redistribute it and/or modify it under the terms of GPLv2

from unittest.mock import patch

import pytest

with patch('shieldnetdefend.common.shieldnet_defend_uid'):
    with patch('shieldnetdefend.common.shieldnet_defend_gid'):
        from shieldnetdefend.core.logtest import send_logtest_msg, validate_dummy_logtest
        from shieldnetdefend.core.common import LOGTEST_SOCKET
        from shieldnetdefend.core.exception import ShieldnetDefendError


@pytest.mark.parametrize('params', [
    {'command': 'random_command', 'parameters': {'param1': 'value1'}},
    {'command': None, 'parameters': None}
])
@patch('shieldnetdefend.core.logtest.ShieldnetDefendSocketJSON.__init__', return_value=None)
@patch('shieldnetdefend.core.logtest.ShieldnetDefendSocketJSON.send')
@patch('shieldnetdefend.core.logtest.ShieldnetDefendSocketJSON.close')
@patch('shieldnetdefend.core.logtest.create_shieldnet_defend_socket_message')
def test_send_logtest_msg(create_message_mock, close_mock, send_mock, init_mock, params):
    """Test `send_logtest_msg` function from module core.logtest.

    Parameters
    ----------
    params : dict
        Params that will be sent to the logtest socket.
    """
    with patch('shieldnetdefend.core.logtest.ShieldnetDefendSocketJSON.receive',
               return_value={'data': {'response': True, 'output': {'timestamp': '1970-01-01T00:00:00.000000-0200'}}}):
        response = send_logtest_msg(**params)
        init_mock.assert_called_with(LOGTEST_SOCKET)
        create_message_mock.assert_called_with(origin={'name': 'Logtest', 'module': 'framework'}, **params)
        assert response == {'data': {'response': True, 'output': {'timestamp': '1970-01-01T02:00:00.000000Z'}}}


@patch('shieldnetdefend.core.logtest.ShieldnetDefendSocketJSON.__init__', return_value=None)
@patch('shieldnetdefend.core.logtest.ShieldnetDefendSocketJSON.send')
@patch('shieldnetdefend.core.logtest.ShieldnetDefendSocketJSON.close')
@patch('shieldnetdefend.core.logtest.create_shieldnet_defend_socket_message')
def test_validate_dummy_logtest(create_message_mock, close_mock, send_mock, init_mock):
    with patch('shieldnetdefend.core.logtest.ShieldnetDefendSocketJSON.receive',
               return_value={'data': {'codemsg': -1}, 'error': 0}):
        with pytest.raises(ShieldnetDefendError) as err_info:
            validate_dummy_logtest()

        assert err_info.value.code == 1113
