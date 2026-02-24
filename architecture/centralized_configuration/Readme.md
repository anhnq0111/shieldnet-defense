<!---
Copyright (C) 2015, ShieldnetDefend Inc.
Created by ShieldnetDefend, Inc. <info@shieldnetdefend.com>.
This program is free software; you can redistribute it and/or modify it under the terms of GPLv2
-->

# Centralized Configuration
## Index
- [Centralized Configuration](#centralized-configuration)
  - [Index](#index)
  - [Purpose](#purpose)
  - [Sequence diagram](#sequence-diagram)

## Purpose

One of the key features of ShieldnetDefend as a EDR is the Centralized Configuration, allowing to deploy configurations, policies, rootcheck descriptions or any other file from ShieldnetDefend Manager to any ShieldnetDefend Agent based on their grouping configuration. This feature has multiples actors: ShieldnetDefend Cluster (Master and Worker nodes), with `shieldnet-defend-remoted` as the main responsible from the managment side, and ShieldnetDefend Agent with `shieldnet-defend-agentd` as resposible from the client side.


## Sequence diagram
Sequence diagram shows the basic flow of Centralized Configuration based on the configuration provided. There are mainly three stages:
1. ShieldnetDefend Manager Master Node (`shieldnet-defend-remoted`) creates every `remoted.shared_reload` (internal) seconds the files that need to be synchronized with the agents.
2. ShieldnetDefend Cluster as a whole (via `shieldnet-defend-clusterd`) continuously synchronize files between ShieldnetDefend Manager Master Node and ShieldnetDefend Manager Worker Nodes
3. ShieldnetDefend Agent `shieldnet-defend-agentd` (via ) sends every `notify_time` (ossec.conf) their status, being `merged.mg` hash part of it. ShieldnetDefend Manager Worker Node (`shieldnet-defend-remoted`) will check if agent's `merged.mg` is out-of-date, and in case this is true, the new `merged.mg` will be pushed to ShieldnetDefend Agent.