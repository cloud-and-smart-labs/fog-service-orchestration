# Python Websocket, Webserver Container and Service (LED) Orchestration with xOpera

Deploying a Python Websocket and Nginx Webserver Container on a swarm of Fog Nodes (Raspberry Pis) and background service (for ON/OFF LED) with a **TOSCA Service Template**. Webserver serves webpage with a button to `ON/OFF LED remotely`.

---
<br>

## Configure with `inputs.yaml` file

### Multiple Manager and Worker
Add list IP address inside `inputs.yaml`
```YAML
manager:
  - 192.168.0.195

workers:
  - 192.168.0.103
  - 192.168.0.165
  - 192.168.0.131
```

### If only one Manager
Keep empty list
```YAML
manager: []
```

### Nodes with actuators
IP Addresses of nodes
```YAML
actuators:
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