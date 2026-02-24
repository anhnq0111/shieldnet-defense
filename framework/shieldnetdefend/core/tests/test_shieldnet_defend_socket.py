# Copyright (C) 2015, ShieldnetDefend Inc.
# Created by ShieldnetDefend, Inc. <info@shieldnetdefend.com>.
# This program is a free software; you can redistribute it and/or modify it under the terms of GPLv2

from unittest.mock import patch, MagicMock

import pytest

from shieldnetdefend.core.exception import ShieldnetDefendException
from shieldnetdefend.core.shieldnet_defend_socket import ShieldnetDefendSocket, ShieldnetDefendSocketJSON, SOCKET_COMMUNICATION_PROTOCOL_VERSION, \
    create_shieldnet_defend_socket_message


@patch('shieldnetdefend.core.shieldnet_defend_socket.ShieldnetDefendSocket._connect')
def test_Shieldnet_DefendSocket__init__(mock_conn):
    """Tests ShieldnetDefendSocket.__init__ function works"""

    ShieldnetDefendSocket('test_path')

    mock_conn.assert_called_once_with()


@patch('shieldnetdefend.core.shieldnet_defend_socket.socket.socket.connect')
def test_Shieldnet_DefendSocket_protected_connect(mock_conn):
    """Tests ShieldnetDefendSocket._connect function works"""

    ShieldnetDefendSocket('test_path')

    mock_conn.assert_called_with('test_path')


@patch('shieldnetdefend.core.shieldnet_defend_socket.socket.socket.connect', side_effect=Exception)
def test_Shieldnet_DefendSocket_protected_connect_ko(mock_conn):
    """Tests ShieldnetDefendSocket._connect function exceptions works"""

    with pytest.raises(ShieldnetDefendException, match=".* 1013 .*"):
        ShieldnetDefendSocket('test_path')


@patch('shieldnetdefend.core.shieldnet_defend_socket.socket.socket.connect')
@patch('shieldnetdefend.core.shieldnet_defend_socket.socket.socket.close')
def test_Shieldnet_DefendSocket_close(mock_close, mock_conn):
    """Tests ShieldnetDefendSocket.close function works"""

    queue = ShieldnetDefendSocket('test_path')

    queue.close()

    mock_conn.assert_called_once_with('test_path')
    mock_close.assert_called_once_with()


@patch('shieldnetdefend.core.shieldnet_defend_socket.socket.socket.connect')
@patch('shieldnetdefend.core.shieldnet_defend_socket.socket.socket.send')
def test_Shieldnet_DefendSocket_send(mock_send, mock_conn):
    """Tests ShieldnetDefendSocket.send function works"""

    queue = ShieldnetDefendSocket('test_path')

    response = queue.send(b"\x00\x01")

    assert isinstance(response, MagicMock)
    mock_conn.assert_called_once_with('test_path')


@pytest.mark.parametrize('msg, effect, send_effect, expected_exception', [
    ('text_msg', 'side_effect', None, 1105),
    (b"\x00\x01", 'return_value', 0, 1014),
    (b"\x00\x01", 'side_effect', Exception, 1014)
])
@patch('shieldnetdefend.core.shieldnet_defend_socket.socket.socket.connect')
def test_Shieldnet_DefendSocket_send_ko(mock_conn, msg, effect, send_effect, expected_exception):
    """Tests ShieldnetDefendSocket.send function exceptions works"""

    queue = ShieldnetDefendSocket('test_path')

    if effect == 'return_value':
        with patch('shieldnetdefend.core.shieldnet_defend_socket.socket.socket.send', return_value=send_effect):
            with pytest.raises(ShieldnetDefendException, match=f'.* {expected_exception} .*'):
                queue.send(msg)
    else:
        with patch('shieldnetdefend.core.shieldnet_defend_socket.socket.socket.send', side_effect=send_effect):
            with pytest.raises(ShieldnetDefendException, match=f'.* {expected_exception} .*'):
                queue.send(msg)

    mock_conn.assert_called_once_with('test_path')


@patch('shieldnetdefend.core.shieldnet_defend_socket.socket.socket.connect')
@patch('shieldnetdefend.core.shieldnet_defend_socket.unpack', return_value='1024')
@patch('shieldnetdefend.core.shieldnet_defend_socket.socket.socket.recv')
def test_Shieldnet_DefendSocket_receive(mock_recv, mock_unpack, mock_conn):
    """Tests ShieldnetDefendSocket.receive function works"""

    queue = ShieldnetDefendSocket('test_path')

    response = queue.receive()

    assert isinstance(response, MagicMock)
    mock_conn.assert_called_once_with('test_path')


@patch('shieldnetdefend.core.shieldnet_defend_socket.socket.socket.connect')
@patch('shieldnetdefend.core.shieldnet_defend_socket.socket.socket.recv', side_effect=Exception)
def test_Shieldnet_DefendSocket_receive_ko(mock_recv, mock_conn):
    """Tests ShieldnetDefendSocket.receive function exception works"""

    queue = ShieldnetDefendSocket('test_path')

    with pytest.raises(ShieldnetDefendException, match=".* 1014 .*"):
        queue.receive()

    mock_conn.assert_called_once_with('test_path')


@patch('shieldnetdefend.core.shieldnet_defend_socket.ShieldnetDefendSocket._connect')
def test_Shieldnet_DefendSocketJSON__init__(mock_conn):
    """Tests ShieldnetDefendSocketJSON.__init__ function works"""

    ShieldnetDefendSocketJSON('test_path')

    mock_conn.assert_called_once_with()


@patch('shieldnetdefend.core.shieldnet_defend_socket.socket.socket.connect')
@patch('shieldnetdefend.core.shieldnet_defend_socket.ShieldnetDefendSocket.send')
def test_Shieldnet_DefendSocketJSON_send(mock_send, mock_conn):
    """Tests ShieldnetDefendSocketJSON.send function works"""

    queue = ShieldnetDefendSocketJSON('test_path')

    response = queue.send('test_msg')

    assert isinstance(response, MagicMock)
    mock_conn.assert_called_once_with('test_path')


@pytest.mark.parametrize('raw', [
    True, False
])
@patch('shieldnetdefend.core.shieldnet_defend_socket.socket.socket.connect')
@patch('shieldnetdefend.core.shieldnet_defend_socket.ShieldnetDefendSocket.receive')
@patch('shieldnetdefend.core.shieldnet_defend_socket.loads', return_value={'error':0, 'message':None, 'data':'Ok'})
def test_Shieldnet_DefendSocketJSON_receive(mock_loads, mock_receive, mock_conn, raw):
    """Tests ShieldnetDefendSocketJSON.receive function works"""
    queue = ShieldnetDefendSocketJSON('test_path')
    response = queue.receive(raw=raw)
    if raw:
        assert isinstance(response, dict)
    else:
        assert isinstance(response, str)
    mock_conn.assert_called_once_with('test_path')


@patch('shieldnetdefend.core.shieldnet_defend_socket.socket.socket.connect')
@patch('shieldnetdefend.core.shieldnet_defend_socket.ShieldnetDefendSocket.receive')
@patch('shieldnetdefend.core.shieldnet_defend_socket.loads', return_value={'error':10000, 'message':'Error', 'data':'KO'})
def test_Shieldnet_DefendSocketJSON_receive_ko(mock_loads, mock_receive, mock_conn):
    """Tests ShieldnetDefendSocketJSON.receive function works"""

    queue = ShieldnetDefendSocketJSON('test_path')

    with pytest.raises(ShieldnetDefendException, match=".* 10000 .*"):
        queue.receive()

    mock_conn.assert_called_once_with('test_path')


@pytest.mark.parametrize('origin, command, parameters', [
    ('origin_sample', 'command_sample', {'sample': 'sample'}),
    (None, 'command_sample', {'sample': 'sample'}),
    ('origin_sample', None, {'sample': 'sample'}),
    ('origin_sample', 'command_sample', None),
    (None, None, None)
])
def test_create_shieldnet_defend_socket_message(origin, command, parameters):
    """Test create_shieldnet_defend_socket_message function."""
    response_message = create_shieldnet_defend_socket_message(origin, command, parameters)
    assert response_message['version'] == SOCKET_COMMUNICATION_PROTOCOL_VERSION
    assert response_message.get('origin') == origin
    assert response_message.get('command') == command
    assert response_message.get('parameters') == parameters
