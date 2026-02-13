# API Reference

The Inventory Harvester module indexes FIM and Inventory data into dedicated indices within the Shieldnet-Defend-indexer (OpenSearch). So the information is retrieved by using the Opensearch API (ref: https://opensearch.org/docs/latest/api-reference/).

For a quick reference, the table below lists the component and its specific query.

| Component                    | Query                                            |
|------------------------------|--------------------------------------------------|
| Inventory OS                 | GET /shieldnet-defend-states-inventory-system-*/_search     |
| Inventory Packages           | GET /shieldnet-defend-states-inventory-packages-*/_search   |
| Inventory Processes          | GET /shieldnet-defend-states-inventory-processes-*/_search  |
| Inventory Ports              | GET /shieldnet-defend-states-inventory-ports-*/_search      |
| Inventory Hardware           | GET /shieldnet-defend-states-inventory-hardware-*/_search   |
| Inventory Hotfixes           | GET /shieldnet-defend-states-inventory-hotfixes-*/_search   |
| Inventory Network Addresses  | GET /shieldnet-defend-states-inventory-networks-*/_search   |
| Inventory Network Protocols  | GET /shieldnet-defend-states-inventory-protocols-*/_search  |
| Inventory Network Interfaces | GET /shieldnet-defend-states-inventory-interfaces-*/_search |

Refer to [Description](description.md) to visualize the retrieved document format for each request.
