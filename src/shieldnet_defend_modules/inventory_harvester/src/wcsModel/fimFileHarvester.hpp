/*
 * ShieldnetDefend inventory harvester
 * Copyright (C) 2015, ShieldnetDefend Inc.
 * January 14, 2025.
 *
 * This program is free software; you can redistribute it
 * and/or modify it under the terms of the GNU General Public
 * License (version 2) as published by the FSF - Free Software
 * Foundation.
 */

#ifndef _FIM_FILE_HARVESTER_HPP
#define _FIM_FILE_HARVESTER_HPP

#include "reflectiveJson.hpp"
#include "wcsClasses/agent.hpp"
#include "wcsClasses/file.hpp"
#include "wcsClasses/shieldnetdefend.hpp"

struct FimFileInventoryHarvester final
{
    File file;
    Agent agent;
    ShieldnetDefend shieldnetdefend;

    REFLECTABLE(MAKE_FIELD("file", &FimFileInventoryHarvester::file),
                MAKE_FIELD("agent", &FimFileInventoryHarvester::agent),
                MAKE_FIELD("shieldnetdefend", &FimFileInventoryHarvester::shieldnetdefend));
};

#endif // _FIM_FILE_HARVESTER_HPP
