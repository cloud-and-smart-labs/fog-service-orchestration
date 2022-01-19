# System Service
Pulls scripts and configuration files from the given URL and creates a background service with `systemctl` command.

## Table of Contents
- [Properties](#properties)
- [Requirements](#requirements)
- [Example](#example)

## Properties
| Property | Type |Purpose |
| --- | --- | --- |
| name | string | Service name |
| script_url | string | Fetch the Python script |
| service_url | string | Fetch the `systemctl` service file |
| packages | list | List of the required Python packages (default empty) |

## Requirements
| Requirement | Type |Purpose |
| --- | --- | --- |
| host | HostedOn | Needs to be hosted on compute node |

## Examples
```yaml
system-service-1:
  type: fog.system.Service
  properties:
    name: service_name
    script_url: https://cloud-and-smart-labs.dev/led-websocket.py
    service_url: https://cloud-and-smart-labs.dev/led-websocket.service
    packages:
      - rpi.gpio
      - websockets
  requirements:
    - host: fog-node-1
    - dependency: docker-service-1
```

```yaml
system-service-1:
  type: fog.system.Service
  properties:
    name: service_name
    script_url: https://cloud-and-smart-labs.dev/led-websocket.py
    service_url: https://cloud-and-smart-labs.dev/led-websocket.service
  requirements:
    - host: fog-node-1
    - dependency: docker-service-1
```