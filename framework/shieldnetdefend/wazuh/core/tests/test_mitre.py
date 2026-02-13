#!/usr/bin/env python
# Copyright (C) 2015, ShieldnetDefend Inc.
# Created by ShieldnetDefend, Inc. <info@shieldnetdefend.com>.
# This program is free software; you can redistribute it and/or modify it under the terms of GPLv2

from unittest.mock import patch

import pytest

from shieldnetdefend.tests.util import InitWDBSocketMock

with patch('shieldnetdefend.core.common.shieldnet_defend_uid'):
    with patch('shieldnetdefend.core.common.shieldnet_defend_gid'):
        from shieldnetdefend.core.mitre import *


@patch('shieldnetdefend.core.utils.ShieldnetDefendDBConnection', return_value=InitWDBSocketMock(sql_schema_file='schema_mitre_test.sql'))
def test_Shieldnet_DefendDBQueryMitreMetadata(mock_wdb):
    """Verify that the method connects correctly to the database and returns the correct type."""
    db_query = ShieldnetDefendDBQueryMitreMetadata()
    data = db_query.run()

    assert isinstance(db_query, ShieldnetDefendDBQueryMitre) and isinstance(data, dict)


@pytest.mark.parametrize('wdb_query_class', [
    ShieldnetDefendDBQueryMitreGroups,
    ShieldnetDefendDBQueryMitreMitigations,
    ShieldnetDefendDBQueryMitreReferences,
    ShieldnetDefendDBQueryMitreTactics,
    ShieldnetDefendDBQueryMitreTechniques,
    ShieldnetDefendDBQueryMitreSoftware

])
@patch('shieldnetdefend.core.utils.ShieldnetDefendDBConnection', return_value=InitWDBSocketMock(sql_schema_file='schema_mitre_test.sql'))
def test_Shieldnet_DefendDBQueryMitre_classes(mock_wdb, wdb_query_class):
    """Verify that the method connects correctly to the database and returns the correct types."""
    db_query = wdb_query_class()
    data = db_query.run()

    assert isinstance(db_query, ShieldnetDefendDBQueryMitre) and isinstance(data, dict)

    # All items have all the related_items (relation_fields) and their type is list
    try:
        assert all(
            isinstance(data_item[related_item], list) for related_item in db_query.relation_fields for data_item in
            data['items'])
    except KeyError:
        pytest.fail("Related item not found in data obtained from query")


@pytest.mark.parametrize('mitre_wdb_query_class', [
    ShieldnetDefendDBQueryMitreGroups,
    ShieldnetDefendDBQueryMitreMitigations,
    ShieldnetDefendDBQueryMitreReferences,
    ShieldnetDefendDBQueryMitreTactics,
    ShieldnetDefendDBQueryMitreTechniques,
    ShieldnetDefendDBQueryMitreSoftware
])
@patch('shieldnetdefend.core.utils.ShieldnetDefendDBConnection')
def test_get_mitre_items(mock_wdb, mitre_wdb_query_class):
    """Test get_mitre_items function."""
    info, data = get_mitre_items(mitre_wdb_query_class)

    db_query_to_compare = mitre_wdb_query_class()

    assert isinstance(info['allowed_fields'], set) and info['allowed_fields'] == set(
        db_query_to_compare.fields.keys()).union(
        db_query_to_compare.relation_fields).union(db_query_to_compare.extra_fields)
    assert isinstance(info['min_select_fields'], set) and info[
        'min_select_fields'] == db_query_to_compare.min_select_fields
