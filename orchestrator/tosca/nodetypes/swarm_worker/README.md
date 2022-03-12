# Swarm Worker
Host node joins the Docker Swarm as Worker node.

## Table of Contents
- [Requirements](#requirements)
- [Capabilities](#capabilities)
- [Example](#example)

## Requirements
| Requirement | Type | Purpose |
| --- | --- | --- |
| host | HostedOn | Needs to be hosted on compute node |
| leader | [TokenTransfer](../../relationshiptypes/token_transfer) (DependsOn) | Needs an authentication token and advertised address for joining Swarm so depends on the [Swarm Leader](../swarm_leader) node |

## Capabilities
| Capability | Type | Purpose |
| --- | --- | --- |
| host | Container | Can host [Docker Containers](../docker_containers) |

## Example
```yaml
docker-swarm-worker-1:
  type: fog.docker.SwarmWorker
  requirements:
    - host: fog-node-2
    - leader: docker-swarm-leader
```