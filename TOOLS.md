# Tools

## Resource Monitoring

- `list_monitoring_resources`: List hosts and services with their real-time status.
- `list_monitoring_entities`: List host groups, service groups, or monitoring servers.
- `count_monitoring_resources_by_status`: Count hosts or services by status.
- `get_host_timeline`: Get the recent event history of a host.
- `get_service_timeline`: Get the recent event history of a service.

## Configuration

- `list_configurations`: List configured hosts, services, and related entities.
- `create_configuration`: Create a new configuration entity.
- `update_configuration`: Update an existing configuration entity.
- `delete_configurations`: Delete one or more configuration entities.
- `manage_monitoring_server_configurations`: Generate or reload poller configurations.

## Monitoring Actions

- `list_monitoring_actions`: List current acknowledgements or downtimes.
- `set_monitoring_actions`: Acknowledge, schedule a downtime, comment, or trigger a check.
- `cancel_monitoring_actions`: Cancel acknowledgements or downtimes.

## Metrics

- `get_service_metrics`: Get a service's current metric values and thresholds.
