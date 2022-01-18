# Container and Service Orchestration on Fog Nodes (Raspberry Pi) with xOpera

**TOSCA Service Templates** for **Dynamic Deployment** of different Fog Computing Services.

---
<br>

## Setup passwordless SSH login
The master node should be able to SSH into other nodes without passwords.
### Generate key pair
```bash
ssh-keygen
```
### Copy the public key to all other nodes
```bash
ssh-copy-id pi@192.168.0.XXX
```
---
## Create virtual environment
### Install dependencies
```bash
sudo apt install python3-venv python3-wheel python-wheel-common
```
### Create .venv
```bash
python3 -m venv .venv
```
### Activate
```bash
source .venv/bin/activate
```
### Install opera packages
```bash
pip install opera==0.6.8
```

### Deactivate
```bash
deactivate
```
---
<br>

## Service orchestration
### Validate
```bash
opera validate -i inputs.yaml service.yaml
```

### Deployment
```bash
opera deploy -i inputs.yaml service.yaml
```

### If deployment fails
```bash
opera deploy -r -i inputs.yaml service.yaml
```

### Undeployment
```bash
opera undeploy
```