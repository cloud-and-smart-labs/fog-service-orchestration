# Python Flask and Privileged Container Orchestration with xOpera

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
Goto: https://suvambasak.github.io/demo