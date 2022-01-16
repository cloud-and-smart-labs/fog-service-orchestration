# Token Transfer
Relationship (dependency) between [Swarm Leader](../../nodetypes/swarm_leader) and [Swarm Worker](../../nodetypes/swarm_worker).

## Table of Contents
- [Attributes](#attributes)

## Attributes
| Attribute | Type |Purpose |
| --- | --- | --- |
| manager_token | string | Join token for Managers |
| worker_token | string | Join token for Workers|
| join_addr_port | string | Advertised address (IP:PORT) for joining swarm cluster eg: `192.168.0.XXX:2377` |
