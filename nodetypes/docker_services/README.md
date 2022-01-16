# Docker Services
Pulls a docker-compose file from the given URL and deploys it on the Docker Swarm from Docker Leader node.

## Table of Contents
- [Properties](#properties)
- [Requirements](#requirements)
- [Example](#example)

## Properties
| Property | Type |Purpose |
| --- | --- | --- |
| name | string | Provide a Docker Stack name |
| url | string | Fetch the `docker-compose.yaml` file |

## Requirements
| Requirement | Type |Purpose |
| --- | --- | --- |
| host | HostedOn | Needs to be hosted on container node |
| dependency | DependsOn | May have a dependency on other [Swarm Worker](../swarm_worker) nodes |

## Example
```yaml
docker-service-1:
  type: fog.docker.Services
  properties:
    name: service_name
    url: https://cloud-and-smart-labs/docker-compose.yaml
  requirements:
    - host: docker-swarm-leader
    - dependency: docker-swarm-worker-1
    - dependency: docker-swarm-worker-2

```