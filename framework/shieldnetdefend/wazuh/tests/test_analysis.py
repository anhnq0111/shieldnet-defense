import sys
from unittest.mock import MagicMock, patch

import pytest

with patch('shieldnetdefend.core.common.shieldnet_defend_uid'):
    with patch('shieldnetdefend.core.common.shieldnet_defend_gid'):
        sys.modules['shieldnetdefend.rbac.orm'] = MagicMock()
        import shieldnetdefend.rbac.decorators

        del sys.modules['shieldnetdefend.rbac.orm']

        from shieldnetdefend.tests.util import RBAC_bypasser

        shieldnetdefend.rbac.decorators.expose_resources = RBAC_bypasser
        from shieldnetdefend import analysis

@pytest.mark.asyncio
@patch('shieldnetdefend.analysis.node_type', 'master')
@patch('shieldnetdefend.analysis.send_reload_ruleset_and_get_results')
async def test_reload_ruleset_master_ok(mock_send_reload_ruleset_msg):
    """Test reload_ruleset() works as expected for master node with successful reload."""
    from shieldnetdefend.core.results import AffectedItemsShieldnetDefendResult
    mock_result = AffectedItemsShieldnetDefendResult()
    mock_result.affected_items.append({'name': 'test-node', 'msg': 'ok'})
    mock_result.total_affected_items = 1
    mock_result._failed_items = {}
    mock_send_reload_ruleset_msg.return_value = mock_result

    result = await analysis.reload_ruleset()
    assert isinstance(result, analysis.AffectedItemsShieldnetDefendResult)
    assert result.total_affected_items == 1
    assert result.failed_items == {}


@pytest.mark.asyncio
@patch('shieldnetdefend.analysis.node_type', 'master')
@patch('shieldnetdefend.analysis.send_reload_ruleset_and_get_results')
async def test_reload_ruleset_master_nok(mock_send_reload_ruleset_msg):
    """Test reload_ruleset() for master node with error in reload."""
    from shieldnetdefend.core.results import AffectedItemsShieldnetDefendResult
    mock_result = AffectedItemsShieldnetDefendResult()
    mock_result._failed_items = {'test-node': {'error': 1914}}
    mock_result._total_failed_items = 1
    mock_send_reload_ruleset_msg.return_value = mock_result

    result = await analysis.reload_ruleset()
    assert isinstance(result, analysis.AffectedItemsShieldnetDefendResult)
    assert result.total_failed_items == 1


@pytest.mark.asyncio
@patch('shieldnetdefend.analysis.node_type', 'worker')
@patch('shieldnetdefend.analysis.local_client.LocalClient')
async def test_reload_ruleset_worker_ok(mock_local_client):
    """Test reload_ruleset() works as expected for worker node with successful reload."""
    # Patch set_reload_ruleset_flag to be async and return a dict with 'success'
    from shieldnetdefend.core.results import AffectedItemsShieldnetDefendResult

    async def async_set_reload_ruleset_flag(lc):
        return {'success': True}

    with patch('shieldnetdefend.analysis.set_reload_ruleset_flag', side_effect=async_set_reload_ruleset_flag):
        result = await analysis.reload_ruleset()
        assert isinstance(result, analysis.AffectedItemsShieldnetDefendResult)
        assert result.total_affected_items == 1
        assert result.failed_items == {}


@pytest.mark.asyncio
@patch('shieldnetdefend.analysis.node_type', 'worker')
@patch('shieldnetdefend.analysis.local_client.LocalClient')
async def test_reload_ruleset_worker_nok(mock_local_client):
    """Test reload_ruleset() for worker node with error in reload."""
    from shieldnetdefend.core.results import AffectedItemsShieldnetDefendResult
    from shieldnetdefend.core.exception import ShieldnetDefendError

    async def async_set_reload_ruleset_flag(lc):
        raise ShieldnetDefendError(1914)

    with patch('shieldnetdefend.analysis.set_reload_ruleset_flag', side_effect=async_set_reload_ruleset_flag):
        result = await analysis.reload_ruleset()
        assert isinstance(result, analysis.AffectedItemsShieldnetDefendResult)
        assert result.total_failed_items == 1
