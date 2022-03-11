from abc import ABC, abstractmethod


class YAMLBuilder(ABC):
    @abstractmethod
    def build(self) -> None:
        pass

    @abstractmethod
    def export(self) -> dict:
        pass


class InputsFile(YAMLBuilder):
    def __init__(self, host_list: list[str]) -> None:
        self.host_list = host_list

    def build(self) -> None:
        self.inputs_yaml = dict()
        for index, host in enumerate(self.host_list):
            self.inputs_yaml[f"node_{index+1}"] = host

    def export(self) -> dict:
        return self.inputs_yaml


class Inputs(YAMLBuilder):
    def __init__(self, input_names: list[str]) -> None:
        self.input_names = input_names

    def build(self) -> None:
        self.template_inputs = {}
        self.template_inputs["inputs"] = dict()
        for name in self.input_names:
            self.template_inputs["inputs"][name] = {"type": "string"}

    def export(self) -> dict:
        return self.template_inputs


class Compute(YAMLBuilder):

    def __init__(self, node_name: str, host: str) -> None:
        self.host = host
        self.node_name = node_name

    def build(self) -> None:
        self.compute_node_yaml = dict()
        self.compute_node_yaml[self.node_name] = {
            "type": "tosca.nodes.Compute",
            "attributes":
            {
                "private_address": {"get_input": self.host},
                "public_address": {"get_input": self.host}
            }
        }

    def export(self) -> dict:
        return self.compute_node_yaml


class SwarmLeader(YAMLBuilder):

    def __init__(self, node_name: str, host_node: str) -> None:
        self.node_name = node_name
        self.host_node = host_node

    def build(self) -> None:
        self.swarm_leader_yaml = dict()
        self.swarm_leader_yaml[self.node_name] = {
            'type': 'fog.docker.SwarmLeader',
            'requirements':
            [
                {'host': self.host_node}
            ]
        }

    def export(self) -> dict:
        return self.swarm_leader_yaml


class SwarmWorker(YAMLBuilder):

    def __init__(self, node_name: str, host_node: str, leader_node: str) -> None:
        self.node_name = node_name
        self.host_node = host_node
        self.leader_node = leader_node

    def build(self) -> None:
        self.swarm_worker_yaml = dict()
        self.swarm_worker_yaml[self.node_name] = {
            'type': 'fog.docker.SwarmWorker',
            'requirements':
            [
                {'host': self.host_node},
                {'leader': self.leader_node}
            ]
        }

    def export(self) -> dict:
        return self.swarm_worker_yaml


class DockerServices(YAMLBuilder):
    def __init__(
        self,
        node_name: str,
        service_name: str,
        url: str,
        host_node: str,
        dependency_nodes: list[str] = []
    ) -> None:

        self.node_name = node_name
        self.service_name = service_name
        self.url = url
        self.host_node = host_node
        self.dependency_nodes = dependency_nodes

    def build(self) -> None:
        self.docker_service_yaml = dict()

        self.docker_service_yaml[self.node_name] = {
            "type": "fog.docker.Services",
            "properties":
            {
                "name": self.service_name,
                "url": self.url
            },
            "requirements": self.build_requirements()
        }

    def build_requirements(self) -> list:
        requirements_list = [{"host": self.host_node}]
        for dependency_node in self.dependency_nodes:
            requirements_list.append({"dependency": dependency_node})

        return requirements_list

    def export(self) -> dict:
        return self.docker_service_yaml


class DockerContainers(YAMLBuilder):
    def __init__(
        self,
        node_name: str,
        compose_name: str,
        url: str,
        host_node: str,
        dependency_nodes: list[str] = [],
        packages: list[str] = []
    ) -> None:

        self.node_name = node_name
        self.compose_name = compose_name
        self.url = url
        self.host_node = host_node
        self.dependency_nodes = dependency_nodes
        self.packages = packages

    def build(self) -> None:
        self.docker_containers_yaml = dict()

        self.docker_containers_yaml[self.node_name] = {
            "type": "fog.docker.Containers",
            "properties": {
                "name": self.compose_name,
                "url": self.url,
                "packages": [package for package in self.packages]
            },
            "requirements": self.build_requirements()
        }

    def build_requirements(self) -> list:
        requirements_list = [{"host": self.host_node}]
        for dependency_node in self.dependency_nodes:
            requirements_list.append({"dependency": dependency_node})

        return requirements_list

    def export(self) -> dict:
        return self.docker_containers_yaml


class SystemService(YAMLBuilder):
    def __init__(
        self,
        node_name: str,
        system_service_name: str,
        script_url: str,
        service_url: str,
        host_node: str,
        dependency_nodes: list[str] = [],
        packages: list[str] = []
    ) -> None:

        self.node_name = node_name
        self.system_service_name = system_service_name
        self.script_url = script_url
        self.service_url = service_url
        self.host_node = host_node
        self.dependency_nodes = dependency_nodes
        self.packages = packages

    def build(self) -> None:
        self.docker_containers_yaml = dict()

        self.docker_containers_yaml[self.node_name] = {
            "type": "fog.system.Service",
            "properties":
            {
                "name": self.system_service_name,
                "script_url": self.script_url,
                "service_url": self.service_url,
                "packages": [package for package in self.packages]
            },
            "requirements": self.build_requirements()
        }

    def build_requirements(self) -> list:
        requirements_list = [{"host": self.host_node}]
        for dependency_node in self.dependency_nodes:
            requirements_list.append({"dependency": dependency_node})

        return requirements_list

    def export(self) -> dict:
        return self.docker_containers_yaml


class Outputs(YAMLBuilder):
    def __init__(self, node_name: str) -> None:
        self.node_name = node_name

    def build(self) -> None:
        self.outputs_yaml = dict()
        self.outputs_yaml["outputs"] = {
            "output_worker_token_attribute":
            {"value": {"get_attribute": [self.node_name, 'worker_token']}},
            "output_manager_token_attribute":
            {"value": {"get_attribute": [self.node_name, "manager_token"]}},
            "advertised_address":
            {"value": {"get_attribute": [self.node_name, "advertise_addr"]}}
        }

    def export(self) -> dict:
        return self.outputs_yaml


class Imports(YAMLBuilder):
    import_index = {
        "fog.docker.SwarmLeader": "nodetypes/swarm_leader/swarm_leader.yaml",
        "fog.docker.SwarmWorker": "nodetypes/swarm_worker/swarm_worker.yaml",
        "fog.docker.Services": "nodetypes/docker_services/docker_services.yaml",
        "fog.docker.Containers": "nodetypes/docker_containers/docker_containers.yaml",
        "fog.system.Service": "nodetypes/system_service/system_service.yaml"
    }

    def __init__(self, node_types: list[str]) -> None:
        self.node_types = node_types
        self.import_set = set()
        self.import_set.add(
            "relationshiptypes/token_transfer/token_transfer.yaml"
        )

    def build(self) -> None:
        for node_type in self.node_types:
            self.import_set.add(self.import_index[node_type])

        self.import_yaml = dict()
        self.import_yaml["imports"] = list(self.import_set)

    def export(self) -> dict:
        return self.import_yaml
