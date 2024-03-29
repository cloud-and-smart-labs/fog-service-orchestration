# Docker Containers
Pulls a docker-compose file from the given URL and deploys it on the host fog node.

## Table of Contents
- [Properties](#properties)
- [Requirements](#requirements)
- [Example](#example)

## Properties
| Property | Type |Purpose |
| --- | --- | --- |
| name | string | Provide a project name |
| url | string | Fetch the `docker-compose.yaml` file |
| packages | list | Python Dependencies (default empty) for the Privileged Container (in case of Sensor/Actuator) |

## Requirements
| Requirement | Type |Purpose |
| --- | --- | --- |
| host | HostedOn | Needs to be hosted on compute node |

## Examples
```yaml
privileged_container-1:
  type: fog.docker.Containers
  properties:
    name: my_proj
    url: https://cloud-and-smart-labs.dev/docker-compose.yaml
    packages:
      - rpi.gpio
      - websockets
  requirements:
    - host: fog-node-1
    - dependency: docker-service-1
```

```yaml
privileged_container-1:
  type: fog.docker.Containers
  properties:
    name: my_proj
    url: https://cloud-and-smart-labs.dev/docker-compose.yaml
  requirements:
    - host: fog-node-1
    - dependency: docker-service-1
```