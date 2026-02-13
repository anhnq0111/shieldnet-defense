# Copyright (C) 2015, ShieldnetDefend Inc.
# Created by ShieldnetDefend, Inc. <info@shieldnetdefend.com>.
# This program is free software; you can redistribute it and/or modify it under the terms of GPLv2

from shieldnetdefend.core import common, mitre
from shieldnetdefend.core.results import AffectedItemsShieldnetDefendResult
from shieldnetdefend.rbac.decorators import expose_resources


@expose_resources(actions=["mitre:read"], resources=["*:*:*"])
def mitre_metadata() -> AffectedItemsShieldnetDefendResult:
    """Return the metadata of the MITRE's database.

    Returns
    -------
    AffectedItemsShieldnetDefendResult
        Metadata of MITRE's db.
    """
    result = AffectedItemsShieldnetDefendResult(none_msg='No MITRE metadata information was returned',
                                      all_msg='MITRE metadata information was returned')

    with mitre.ShieldnetDefendDBQueryMitreMetadata() as db_query:
        data = db_query.run()

    result.affected_items.extend(data['items'])
    result.total_affected_items = data['totalItems']

    return result


@expose_resources(actions=["mitre:read"], resources=["*:*:*"])
def mitre_mitigations(filters: dict = None, offset: int = 0, limit: int = common.DATABASE_LIMIT, select: list = None,
                      sort_by: dict = None, sort_ascending: bool = True, search_text: str = None,
                      complementary_search: bool = False, search_in_fields: list = None,
                      q: str = '', distinct: bool = False) -> AffectedItemsShieldnetDefendResult:
    """Get information of specified MITRE's mitigations and its relations.

    Parameters
    ----------
    filters : dict
        Define field filters required by the user. Format: {"field1":"value1", "field2":["value2","value3"]}
    offset : int
        First item to return.
    limit : int
        Maximum number of items to return.
    select : list
        Select which fields to return (separated by comma).
    sort_by : dict
        Fields to sort the items by. Format: {"fields":["field1","field2"],"order":"asc|desc"}
    sort_ascending : bool
        Sort in ascending (true) or descending (false) order.
    search_text : str
        Text to search.
    complementary_search : bool
        Find items without the text to search.
    search_in_fields : list
        Fields to search in.
    q : str
        Query for filtering a list of results.
    distinct : bool
        Look for distinct values.

    Returns
    -------
    AffectedItemsShieldnetDefendResult
        Dictionary with the information of the specified mitigations and their relationships.
    """
    data = mitre.get_results_with_select(mitre.ShieldnetDefendDBQueryMitreMitigations, **locals())

    result = AffectedItemsShieldnetDefendResult(none_msg='No MITRE mitigations information was returned',
                                      all_msg='MITRE mitigations information was returned')
    result.affected_items.extend(data['items'])
    result.total_affected_items = data['totalItems']

    return result


@expose_resources(actions=["mitre:read"], resources=["*:*:*"])
def mitre_references(filters: dict = None, offset: int = 0, limit: int = common.DATABASE_LIMIT, select: list = None,
                     sort_by: dict = None, sort_ascending: bool = True, search_text: str = None,
                     complementary_search: bool = False, search_in_fields: list = None,
                     q: str = '') -> AffectedItemsShieldnetDefendResult:
    """Get information of specified MITRE's references.

    Parameters
    ----------
    filters : dict
        Define field filters required by the user. Format: {"field1":"value1", "field2":["value2","value3"]}
    offset : int
        First item to return.
    limit : int
        Maximum number of items to return.
    select : list
        Select which fields to return (separated by comma).
    sort_by : dict
        Fields to sort the items by. Format: {"fields":["field1","field2"],"order":"asc|desc"}
    sort_ascending : bool
        Sort in ascending (true) or descending (false) order.
    search_text : str
        Text to search.
    complementary_search : bool
        Find items without the text to search.
    search_in_fields : list
        Fields to search in.
    q : str
        Query for filtering a list of results.

    Returns
    -------
    AffectedItemsShieldnetDefendResult
        Dictionary with the information of the specified references.
    """
    data = mitre.get_results_with_select(mitre.ShieldnetDefendDBQueryMitreReferences, **locals())

    result = AffectedItemsShieldnetDefendResult(none_msg='No MITRE references information was returned',
                                      all_msg='MITRE references information was returned')
    result.affected_items.extend(data['items'])
    result.total_affected_items = data['totalItems']

    return result


@expose_resources(actions=["mitre:read"], resources=["*:*:*"])
def mitre_techniques(filters: dict = None, offset: int = 0, limit: int = common.DATABASE_LIMIT, select: list = None,
                     sort_by: dict = None, sort_ascending: bool = True, search_text: str = None,
                     complementary_search: bool = False, search_in_fields: list = None,
                     q: str = '', distinct: bool = False) -> AffectedItemsShieldnetDefendResult:
    """Get information of specified MITRE's techniques and its relations.

    Parameters
    ----------
    filters : dict
        Define field filters required by the user. Format: {"field1":"value1", "field2":["value2","value3"]}
    offset : int
        First item to return.
    limit : int
        Maximum number of items to return.
    select : list
        Select which fields to return (separated by comma).
    sort_by : dict
        Fields to sort the items by. Format: {"fields":["field1","field2"],"order":"asc|desc"}
    sort_ascending : bool
        Sort in ascending (true) or descending (false) order.
    search_text : str
        Text to search.
    complementary_search : bool
        Find items without the text to search.
    search_in_fields : list
        Fields to search in.
    q : str
        Query for filtering a list of results.
    distinct : bool
        Look for distinct values.

    Returns
    -------
    AffectedItemsShieldnetDefendResult
        Dictionary with the information of the specified techniques and their relationships.
    """
    data = mitre.get_results_with_select(mitre.ShieldnetDefendDBQueryMitreTechniques, **locals())

    result = AffectedItemsShieldnetDefendResult(none_msg='No MITRE techniques information was returned',
                                      all_msg='MITRE techniques information was returned')
    result.affected_items.extend(data['items'])
    result.total_affected_items = data['totalItems']

    return result


@expose_resources(actions=["mitre:read"], resources=["*:*:*"])
def mitre_tactics(filters: dict = None, offset: int = 0, limit: int = common.DATABASE_LIMIT, select: list = None,
                  sort_by: dict = None, sort_ascending: bool = True, search_text: str = None,
                  complementary_search: bool = False, search_in_fields: list = None,
                  q: str = '', distinct: bool = False) -> AffectedItemsShieldnetDefendResult:
    """Get information of specified MITRE's tactics and its relations.

    Parameters
    ----------
    filters : dict
        Define field filters required by the user. Format: {"field1":"value1", "field2":["value2","value3"]}
    offset : int
        First item to return.
    limit : int
        Maximum number of items to return.
    select : list
        Select which fields to return (separated by comma).
    sort_by : dict
        Fields to sort the items by. Format: {"fields":["field1","field2"],"order":"asc|desc"}
    sort_ascending : bool
        Sort in ascending (true) or descending (false) order.
    search_text : str
        Text to search.
    complementary_search : bool
        Find items without the text to search.
    search_in_fields : list
        Fields to search in.
    q : str
        Query for filtering a list of results.
    distinct : bool
        Look for distinct values.

    Returns
    -------
    AffectedItemsShieldnetDefendResult
        Dictionary with the information of the specified tactics and their relationships.
    """
    data = mitre.get_results_with_select(mitre.ShieldnetDefendDBQueryMitreTactics, **locals())

    result = AffectedItemsShieldnetDefendResult(none_msg='No tactics information was returned',
                                      all_msg='All tactics information was returned')
    result.affected_items.extend(data['items'])
    result.total_affected_items = data['totalItems']

    return result


@expose_resources(actions=["mitre:read"], resources=["*:*:*"])
def mitre_groups(filters: dict = None, offset: int = 0, limit: int = common.DATABASE_LIMIT, select: list = None,
                 sort_by: dict = None, sort_ascending: bool = True, search_text: str = None,
                 complementary_search: bool = False, search_in_fields: list = None,
                 q: str = '', distinct: bool = False) -> AffectedItemsShieldnetDefendResult:
    """Get information of specified MITRE's groups and its relations.

    Parameters
    ----------
    filters : dict
        Define field filters required by the user. Format: {"field1":"value1", "field2":["value2","value3"]}
    offset : int
        First item to return.
    limit : int
        Maximum number of items to return.
    select : list
        Select which fields to return (separated by comma).
    sort_by : dict
        Fields to sort the items by. Format: {"fields":["field1","field2"],"order":"asc|desc"}
    sort_ascending : bool
        Sort in ascending (true) or descending (false) order.
    search_text : str
        Text to search.
    complementary_search : bool
        Find items without the text to search.
    search_in_fields : list
        Fields to search in.
    q : str
        Query for filtering a list of results.
    distinct : bool
        Look for distinct values.

    Returns
    -------
    AffectedItemsShieldnetDefendResult
        Dictionary with the information of the specified groups and their relationships.
    """
    data = mitre.get_results_with_select(mitre.ShieldnetDefendDBQueryMitreGroups, **locals())

    result = AffectedItemsShieldnetDefendResult(none_msg='No MITRE groups information was returned',
                                      all_msg='MITRE groups information was returned')
    result.affected_items.extend(data['items'])
    result.total_affected_items = data['totalItems']

    return result


@expose_resources(actions=["mitre:read"], resources=["*:*:*"])
def mitre_software(filters: dict = None, offset: int = 0, limit: int = common.DATABASE_LIMIT, select: list = None,
                   sort_by: dict = None, sort_ascending: bool = True, search_text: str = None,
                   complementary_search: bool = False, search_in_fields: list = None,
                   q: str = '', distinct: bool = False) -> AffectedItemsShieldnetDefendResult:
    """Get information of specified MITRE's software and its relations.

    Parameters
    ----------
    filters : dict
        Define field filters required by the user. Format: {"field1":"value1", "field2":["value2","value3"]}
    offset : int
        First item to return.
    limit : int
        Maximum number of items to return.
    select : list
        Select which fields to return (separated by comma).
    sort_by : dict
        Fields to sort the items by. Format: {"fields":["field1","field2"],"order":"asc|desc"}
    sort_ascending : bool
        Sort in ascending (true) or descending (false) order.
    search_text : str
        Text to search.
    complementary_search : bool
        Find items without the text to search.
    search_in_fields : list
        Fields to search in.
    q : str
        Query for filtering a list of results.
    distinct : bool
        Look for distinct values.

    Returns
    -------
    AffectedItemsShieldnetDefendResult
        Dictionary with the information of the specified software and their relationships.
    """
    data = mitre.get_results_with_select(mitre.ShieldnetDefendDBQueryMitreSoftware, **locals())

    result = AffectedItemsShieldnetDefendResult(none_msg='No MITRE software information was returned',
                                      all_msg='MITRE software information was returned')
    result.affected_items.extend(data['items'])
    result.total_affected_items = data['totalItems']

    return result
