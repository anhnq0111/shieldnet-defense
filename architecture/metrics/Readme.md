<!---
Copyright (C) 2015, ShieldnetDefend Inc.
Created by ShieldnetDefend, Inc. <info@shieldnetdefend.com>.
This program is free software; you can redistribute it and/or modify it under the terms of GPLv2
-->

# Metrics

## Index

- [Metrics](#metrics)
  - [Index](#index)
  - [Purpose](#purpose)
  - [Sequence diagram](#sequence-diagram)

## Purpose

ShieldnetDefend includes some metrics to understand the behavior of its components, which allow to investigate errors and detect problems with some configurations. This feature has multiple actors: `shieldnet-defend-remoted` for agent interaction messages, `shieldnet-defend-analysisd` for processed events.

## Sequence diagram

The sequence diagram shows the basic flow of metric counters. These are the main flows:

1. Messages received by `shieldnet-defend-remoted` from agents.
2. Messages that `shieldnet-defend-remoted` sends to agents.
3. Events received by `shieldnet-defend-analysisd`.
4. Events processed by `shieldnet-defend-analysisd`.
