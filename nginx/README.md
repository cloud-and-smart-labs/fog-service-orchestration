# Nginx Container Orchestration with xOpera

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
The port 9000 will be mapped to port 80
```YAML
port: 9000
```
### Number of replicas
Total 7 container will be started
```YAML
replicas: 7
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