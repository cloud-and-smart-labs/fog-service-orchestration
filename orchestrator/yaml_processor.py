import yaml
from config import Configuration


def create_input_file() -> None:
    "Creates inputs.yaml file"
    with open(Configuration.get_host_file_path()) as host_file:
        hosts = host_file.read().strip().split("\n")

        inputs_yaml = {}
        for index, host in enumerate(hosts):
            inputs_yaml[f"node_{index+1}"] = host

        with open(Configuration.get_inputs_yaml_file_path(), "w") as inputs_yaml_file:
            inputs_yaml_file.write(yaml.dump(inputs_yaml))
