# Copyright (C) 2015, ShieldnetDefend Inc.
# Created by ShieldnetDefend, Inc. <info@shieldnetdefend.com>.
# This program is free software; you can redistribute it and/or modify it under the terms of GPLv2

from shieldnetdefend import common
from shieldnetdefend.core.agent import get_agents_info, get_rbac_filters, ShieldnetDefendDBQueryAgents
from shieldnetdefend.core.exception import ShieldnetDefendError, ShieldnetDefendResourceNotFound
from shieldnetdefend.core.results import AffectedItemsShieldnetDefendResult
from shieldnetdefend.core.rootcheck import ShieldnetDefendDBQueryRootcheck, last_scan, rootcheck_delete_agent
from shieldnetdefend.core.shieldnet_defend_queue import ShieldnetDefendQueue
from shieldnetdefend.core.wdb import ShieldnetDefendDBConnection
from shieldnetdefend.rbac.decorators import expose_resources


@expose_resources(actions=["rootcheck:run"], resources=["agent:id:{agent_list}"],
                  post_proc_kwargs={'exclude_codes': [1701, 1707]})
def run(agent_list: list = None) -> AffectedItemsShieldnetDefendResult:
    """Run a rootcheck scan in the specified agents.

    Parameters
    ----------
    agent_list : list
         List of the agents IDs to run the scan for.

    Returns
    -------
    AffectedItemsShieldnetDefendResult
        JSON containing the affected agents.
    """
    result = AffectedItemsShieldnetDefendResult(all_msg='Rootcheck scan was restarted on returned agents',
                                      some_msg='Rootcheck scan was not restarted on some agents',
                                      none_msg='No rootcheck scan was restarted')

    system_agents = get_agents_info()
    rbac_filters = get_rbac_filters(system_resources=system_agents, permitted_resources=agent_list)
    agent_list = set(agent_list)
    not_found_agents = agent_list - system_agents

    # Add non existent agents to failed_items
    [result.add_failed_item(id_=agent, error=ShieldnetDefendResourceNotFound(1701)) for agent in not_found_agents]

    # Add non eligible agents to failed_items
    with ShieldnetDefendDBQueryAgents(limit=None, select=["id", "status"], query=f'status!=active', **rbac_filters) as db_query:
        non_eligible_agents = db_query.run()['items']

    [result.add_failed_item(
        id_=agent['id'],
        error=ShieldnetDefendError(1707)) for agent in non_eligible_agents]

    with ShieldnetDefendQueue(common.AR_SOCKET) as wq:
        eligible_agents = agent_list - not_found_agents - {d['id'] for d in non_eligible_agents}
        for agent_id in eligible_agents:
            try:
                wq.send_msg_to_agent(ShieldnetDefendQueue.HC_SK_RESTART, agent_id)
                result.affected_items.append(agent_id)
            except ShieldnetDefendError as e:
                result.add_failed_item(id_=agent_id, error=e)

    result.affected_items.sort(key=int)
    result.total_affected_items = len(result.affected_items)

    return result


@expose_resources(actions=["rootcheck:clear"], resources=["agent:id:{agent_list}"])
def clear(agent_list: list = None) -> AffectedItemsShieldnetDefendResult:
    """Clear the rootcheck database for a list of agents.

    Parameters
    ----------
    agent_list : list
        List of agent ids.

    Returns
    -------
    AffectedItemsShieldnetDefendResult
        JSON containing the affected agents.
    """
    result = AffectedItemsShieldnetDefendResult(all_msg='Rootcheck database was cleared on returned agents',
                                      some_msg='Rootcheck database was not cleared on some agents',
                                      none_msg="No rootcheck database was cleared")

    wdb_conn = ShieldnetDefendDBConnection()
    system_agents = get_agents_info()
    agent_list = set(agent_list)
    not_found_agents = agent_list - system_agents
    # Add non existent agents to failed_items
    [result.add_failed_item(id_=agent_id, error=ShieldnetDefendResourceNotFound(1701)) for agent_id in not_found_agents]

    eligible_agents = agent_list - not_found_agents
    for agent_id in eligible_agents:
        try:
            rootcheck_delete_agent(agent_id, wdb_conn)
            result.affected_items.append(agent_id)
        except ShieldnetDefendError as e:
            result.add_failed_item(id_=agent_id, error=e)

    result.affected_items.sort(key=int)
    result.total_affected_items = len(result.affected_items)

    return result


@expose_resources(actions=["rootcheck:read"], resources=["agent:id:{agent_list}"])
def get_last_scan(agent_list: list) -> AffectedItemsShieldnetDefendResult:
    """Get the last rootcheck scan of an agent.

    Parameters
    ----------
    agent_list : list
        List with the agent ID to get the last scan date from.

    Returns
    -------
    AffectedItemsShieldnetDefendResult
        JSON containing the scan date.
    """
    result = AffectedItemsShieldnetDefendResult(all_msg='Last rootcheck scan of the agent was returned',
                                      none_msg='No last scan information was returned')

    result.affected_items.append(last_scan(agent_list[0]))
    result.total_affected_items = len(result.affected_items)

    return result


@expose_resources(actions=["rootcheck:read"], resources=["agent:id:{agent_list}"])
def get_rootcheck_agent(agent_list: list = None, offset: int = 0, limit: int = common.DATABASE_LIMIT, sort: str = None,
                        search: str = None, select: str = None, filters: dict = None, q: str = '',
                        distinct: bool = False) -> AffectedItemsShieldnetDefendResult:
    """Return a list of events from the rootcheck database.

    Parameters
    ----------
    agent_list : list
        Agent ID to get the rootcheck events from.
    offset : int
        First element to return in the collection.
    limit : int
        Maximum number of elements to return.
    sort : str
        Sort the collection by a field or fields (separated by comma). Use +/- at the beginning to list in
        ascending or descending order.
    search : str
        Look for elements with the specified string.
    select : str
        Select which fields to return (separated by comma).
    q : str
        Query to filter results by.
    distinct : bool
        Look for distinct values.
    filters : dict
        Fields to filter by.

    Returns
    -------
    AffectedItemsShieldnetDefendResult
        JSON containing the rootcheck events.
    """
    if filters is None:
        filters = {}
    result = AffectedItemsShieldnetDefendResult(all_msg='All selected rootcheck information was returned',
                                      some_msg='Some rootcheck information was not returned',
                                      none_msg='No rootcheck information was returned'
                                      )

    with ShieldnetDefendDBQueryRootcheck(agent_id=agent_list[0], offset=offset, limit=limit, sort=sort, search=search,
                               select=select, count=True, get_data=True, query=q, filters=filters,
                               distinct=distinct) as db_query:
        data = db_query.run()

    result.affected_items.extend(data['items'])
    result.total_affected_items = data['totalItems']

    return result
