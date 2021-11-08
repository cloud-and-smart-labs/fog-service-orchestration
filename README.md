# Container Orchestration with xOpera

## Create virtual environment
```bash
$ sudo apt install python3-venv python3-wheel python-wheel-common
$ python3 -m venv .venv
$ source .venv/bin/activate

$ pip install -r requirements.txt 


$ deactivate
```


## Validate
```bash
# opera validate -i inputs.yaml service.yaml
```

## Deployment
```bash
# opera deploy -i inputs.yaml service.yaml
```

## If deployment fails
```bash
# opera deploy -r -i inputs.yaml service.yaml
```

## Undeployment
```bash
# opera undeploy
```