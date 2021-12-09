# Python Websocket, Webserver Container and Privileged Container (LED) Orchestration with xOpera

Deploying a Python Websocket and Nginx Webserver Container on a swarm of Fog Nodes (Raspberry Pis) and Privileged Containers (for ON/OFF LED) with a **TOSCA Service Template**. Webserver serves webpage with a button to `ON/OFF LED remotely`.

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
### Permission change
```BASH
chmod +x validate.sh deploy.sh undeploy.sh
```

### Validate
```BASH
./validate.sh
```
### Deployment
```BASH
./deploy.sh
```
### Undeployment
```BASH
./undeploy.sh
```
## Web
Goto: https://suvambasak.github.io/fog-service-orchestration