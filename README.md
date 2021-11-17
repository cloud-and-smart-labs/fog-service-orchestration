# Container Orchestration with xOpera

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
### Install packages
```bash
pip install opera
```

### Deactivate
```bash
deactivate
```
---
## Validate
```bash
opera validate -i inputs.yaml service.yaml
```

## Deployment
```bash
opera deploy -i inputs.yaml service.yaml
```

## If deployment fails
```bash
opera deploy -r -i inputs.yaml service.yaml
```

## Undeployment
```bash
opera undeploy
```