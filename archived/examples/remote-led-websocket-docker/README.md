# Python Websocket, Webserver Container and Privileged Container (LED) Orchestration with xOpera

Deploying a Python Websocket and Nginx Webserver Container on a swarm of Fog Nodes (Raspberry Pis) and Privileged Containers (for ON/OFF LED) with a **TOSCA Service Template**. Webserver serves webpage with a button to `ON/OFF LED remotely`.

---
<br>

## Configure with `inputs.yaml` file

### Multiple Manager and Worker
Add list IP address inside `inputs.yaml`
```YAML
managers:
  - 192.168.0.195

workers:
  - 192.168.0.103
  - 192.168.0.165
  - 192.168.0.131
```

### If only one Manager
Keep empty list
```YAML
managers: []
```

### Nodes with sensors and actuators
IP Addresses of nodes
```YAML
privileged_nodes:
  - 192.168.0.222
  - 192.168.0.112
```
---
<br>

## Deployment of Service
### Validate
```BASH
opera validate -i inputs.yaml service.yaml
```
### Deployment
```BASH
opera deploy -i inputs.yaml service.yaml
```
### Undeployment
```BASH
opera undeploy
```