# Tools

| Tool                                      | Role     | Description                                                    |
| ----------------------------------------- | -------- | -------------------------------------------------------------- |
| **Resource Monitoring**                                                                                               |
| `list_monitoring_resources`               | `READER` | List hosts and services with their real-time status.           |
| `list_monitoring_entities`                | `READER` | List host groups, service groups, or monitoring servers.       |
| `count_monitoring_resources_by_status`    | `READER` | Count hosts or services by status.                             |
| `get_host_timeline`                       | `READER` | Get the recent event history of a host.                        |
| `get_service_timeline`                    | `READER` | Get the recent event history of a service.                     |
| **Configuration**                         |          |                                                                |
| `list_configurations`                     | `READER` | List configured hosts, services, and related entities.         |
| `create_configuration`                    | `EDITOR` | Create a new configuration entity.                             |
| `update_configuration`                    | `EDITOR` | Update an existing configuration entity.                       |
| `delete_configurations`                   | `ADMIN`  | Delete one or more configuration entities.                     |
| `manage_monitoring_server_configurations` | `ADMIN`  | Generate or reload poller configurations.                      |
| **Monitoring Actions**                    |          |                                                                |
| `list_monitoring_actions`                 | `READER` | List current acknowledgements or downtimes.                    |
| `set_monitoring_actions`                  | `EDITOR` | Acknowledge, schedule a downtime, comment, or trigger a check. |
| `cancel_monitoring_actions`               | `EDITOR` | Cancel acknowledgements or downtimes.                          |
| **Metrics**                               |          |                                                                |
| `get_service_metrics`                     | `READER` | Get a service's current metric values and thresholds.          |
