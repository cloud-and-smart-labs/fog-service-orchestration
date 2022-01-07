# Python Flask and Privileged Container (LED Blink) Orchestration with xOpera

Deploying a Python Flask Container on a swarm of Fog Nodes (Raspberry Pis) and Privileged Containers (for blinking LED) with a **TOSCA Service Template**. Privileged Containers get the frequency of blinking from the Flask API running in Swarm.

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

### Port mapping
The port 80 will be mapped to port 80
```YAML
port: 80
```
### Number of replicas
Total 7 container will be started
```YAML
replicas: 7
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