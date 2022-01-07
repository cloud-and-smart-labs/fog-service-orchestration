# Python Flask Container Orchestration with xOpera

Deploying a Python Flask Container on a swarm of Fog Nodes (Raspberry Pis) with a **TOSCA Service Template**.

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