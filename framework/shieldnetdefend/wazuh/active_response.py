# Copyright (C) 2015, ShieldnetDefend Inc.
# Created by ShieldnetDefend, Inc. <info@shieldnetdefend.com>.
# This program is free software; you can redistribute it and/or modify it under the terms of GPLv2

from shieldnetdefend.core import active_response, common
from shieldnetdefend.core.agent import get_agents_info
from shieldnetdefend.core.exception import ShieldnetDefendException, ShieldnetDefendError, ShieldnetDefendResourceNotFound
from shieldnetdefend.core.shieldnet_defend_queue import ShieldnetDefendQueue
from shieldnetdefend.core.results import AffectedItemsShieldnetDefendResult
from shieldnetdefend.rbac.decorators import expose_resources


@expose_resources(actions=['active-response:command'], resources=['agent:id:{agent_list}'],
                  post_proc_kwargs={'exclude_codes': [1701, 1703]})
def run_command(agent_list: list = None, command: str = '', arguments: list = None,
                alert: dict = None) -> AffectedItemsShieldnetDefendResult:
    """Run AR command in a specific agent.

    Parameters
    ----------
    agent_list : list
        Agents list that will run the AR command.
    command : str
        Command running in the agents. If this value starts with !, then it refers to a script name instead of a
        command name.
    custom : bool
        Whether the specified command is a custom command or not.
    arguments : list
        Command arguments.
    alert : dict
        Alert information depending on the AR executed.

    Returns
    -------
    AffectedItemsShieldnetDefendResult
        Affected items.
    """
    result = AffectedItemsShieldnetDefendResult(all_msg='AR command was sent to all agents',
                                      some_msg='AR command was not sent to some agents',
                                      none_msg='AR command was not sent to any agent'
                                      )
    if agent_list:
        with ShieldnetDefendQueue(common.AR_SOCKET) as wq:
            system_agents = get_agents_info()
            for agent_id in agent_list:
                try:
                    if agent_id not in system_agents:
                        raise ShieldnetDefendResourceNotFound(1701)
                    if agent_id == "000":
                        raise ShieldnetDefendError(1703)
                    active_response.send_ar_message(agent_id, wq, command, arguments, alert)
                    result.affected_items.append(agent_id)
                    result.total_affected_items += 1
                except ShieldnetDefendException as e:
                    result.add_failed_item(id_=agent_id, error=e)
            result.affected_items.sort(key=int)

    return result
