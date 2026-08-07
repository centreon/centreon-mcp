# Tools

## Resource Monitoring

| Name                                   | Description                                                                                                                                                |
| -------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `list_monitoring_resources`            | Query real-time monitoring data (hosts and services) with rich filtering (status, status type, name/alias, output content, scope), paginated and sortable. |
| `list_monitoring_entities`             | List host groups, service groups, or monitoring servers (pollers), filterable by their attributes.                                                         |
| `count_monitoring_resources_by_status` | Return the total number of hosts or services in each status, optionally scoped by host, group, or category.                                                |
| `get_host_timeline`                    | Fetch a host's event history (state changes, notifications, downtimes, acknowledgements, comments), filterable and sorted by date.                         |
| `get_service_timeline`                 | Fetch a service's event history (state changes, notifications, downtimes, acknowledgements, comments), filterable and sorted by date.                      |

## Configuration

| Name                                      | Description                                                                                            |
| ----------------------------------------- | ------------------------------------------------------------------------------------------------------ |
| `list_configurations`                     | List configurations, filterable by entity-specific fields, paginated and sortable.                     |
| `create_configuration`                    | Create a new configuration for the chosen entity type.                                                 |
| `update_configuration`                    | Partially update an existing configuration by ID, using only the fields that change.                   |
| `delete_configurations`                   | Delete one or more configurations by their IDs.                                                        |
| `manage_monitoring_server_configurations` | Generate or reload the configuration files for one or more pollers (or all pollers if none specified). |

## Monitoring Actions

| Name                        | Description                                                                                                        |
| --------------------------- | ------------------------------------------------------------------------------------------------------------------ |
| `list_monitoring_actions`   | List current acknowledgements or downtimes, with pagination and sorting.                                           |
| `set_monitoring_actions`    | Acknowledge, schedule a downtime, attach a comment, or trigger a check without waiting for the next polling cycle. |
| `cancel_monitoring_actions` | Cancel one or more acknowledgements or downtimes by their IDs.                                                     |

## Metrics

| Name                  | Description                                                                                          |
| --------------------- | ---------------------------------------------------------------------------------------------------- |
| `get_service_metrics` | Retrieve all metrics of a service with their current values, units, and warning/critical thresholds. |
