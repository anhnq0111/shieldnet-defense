/*
 * ShieldnetDefend inventory harvester
 * Copyright (C) 2015, ShieldnetDefend Inc.
 * March 27, 2025.
 *
 * This program is free software; you can redistribute it
 * and/or modify it under the terms of the GNU General Public
 * License (version 2) as published by the FSF - Free Software
 * Foundation.
 */

#ifndef _INVENTORY_NETWORK_PROTOCOL_HARVESTER_HPP
#define _INVENTORY_NETWORK_PROTOCOL_HARVESTER_HPP

#include "reflectiveJson.hpp"
#include "wcsClasses/agent.hpp"
#include "wcsClasses/networkProtocol.hpp"
#include "wcsClasses/shieldnetdefend.hpp"

struct InventoryNetworkProtocolHarvester final
{
    struct Interface final
    {
        std::string_view name;

        REFLECTABLE(MAKE_FIELD("name", &Interface::name));
    };

    Interface interface;

    Agent agent;
    Network network;
    ShieldnetDefend shieldnetdefend;

    REFLECTABLE(MAKE_FIELD("network", &InventoryNetworkProtocolHarvester::network),
                MAKE_FIELD("interface", &InventoryNetworkProtocolHarvester::interface),
                MAKE_FIELD("agent", &InventoryNetworkProtocolHarvester::agent),
                MAKE_FIELD("shieldnetdefend", &InventoryNetworkProtocolHarvester::shieldnetdefend));
};

#endif // _INVENTORY_NETWORK_PROTOCOL_HARVESTER_HPP
