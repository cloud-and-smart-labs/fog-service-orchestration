# Swarm Leader
Initiates Docker Swarm on the host node and becomes Swarm Manager.

## Table of Contents
- [Attributes](#attributes)
- [Requirements](#requirements)
- [Capabilities](#capabilities)
- [Example](#example)

## Attributes
| Property | Type | Purpose |
| --- | --- | --- |
| manager_token | string | Join token for Managers |
| worker_token | string | Join token for Workers |
| advertise_addr | string | Advertised address (IP:PORT) for joining swarm cluster eg: `192.168.0.XXX:2377` |

## Requirements
| Requirement | Type | Purpose |
| --- | --- | --- |
| host | HostedOn | Needs to be hosted on compute node |

## Capabilities
| Capability | Type | Purpose |
| --- | --- | --- |
| host | Container | Can host [Docker Services](../docker_services) |

## Example
```yaml
docker-swarm-leader:
  type: fog.docker.SwarmLeader
  requirements:
    - host: fog-node-1
```