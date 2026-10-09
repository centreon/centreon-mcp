# Tools

Each tool requires a permission level. Users are granted the tools at or below their own level, and
tools above it are hidden from them. Deployments that do not authenticate their users expose every
tool. See [Authentication](README.md#authentication).

## Resource Monitoring

| Tool                                   | Minimum role | Description                                              |
| -------------------------------------- | ------------ | -------------------------------------------------------- |
| `list_monitoring_resources`            | `reader`     | List hosts and services with their real-time status.     |
| `list_monitoring_entities`             | `reader`     | List host groups, service groups, or monitoring servers. |
| `count_monitoring_resources_by_status` | `reader`     | Count hosts or services by status.                       |
| `get_host_timeline`                    | `reader`     | Get the recent event history of a host.                  |
| `get_service_timeline`                 | `reader`     | Get the recent event history of a service.               |

## Configuration

| Tool                                      | Minimum role | Description                                            |
| ----------------------------------------- | ------------ | ------------------------------------------------------ |
| `list_configurations`                     | `reader`     | List configured hosts, services, and related entities. |
| `create_configuration`                    | `editor`     | Create a new configuration entity.                     |
| `update_configuration`                    | `editor`     | Update an existing configuration entity.               |
| `delete_configurations`                   | `admin`      | Delete one or more configuration entities.             |
| `manage_monitoring_server_configurations` | `admin`      | Generate or reload poller configurations.              |

## Monitoring Actions

| Tool                        | Minimum role | Description                                                    |
| --------------------------- | ------------ | -------------------------------------------------------------- |
| `list_monitoring_actions`   | `reader`     | List current acknowledgements or downtimes.                    |
| `set_monitoring_actions`    | `editor`     | Acknowledge, schedule a downtime, comment, or trigger a check. |
| `cancel_monitoring_actions` | `editor`     | Cancel acknowledgements or downtimes.                          |

## Metrics

| Tool                  | Minimum role | Description                                           |
| --------------------- | ------------ | ----------------------------------------------------- |
| `get_service_metrics` | `reader`     | Get a service's current metric values and thresholds. |

## Account

| Tool                  | Minimum role | Description                                                                     |
| --------------------- | ------------ | ------------------------------------------------------------------------------- |
| `get_current_context` | none         | Get the Centreon the tools act on and the permission level of the current user. |
