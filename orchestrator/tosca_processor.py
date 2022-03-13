from config import Configuration
from io_operation import FileHandler, NetworkHandler
from abc import ABC, abstractmethod


class TOSCAProcessor:
    """
    Create inputs.yaml file from the system HOST file (orchestrator.config.py) &
    Creates TOSCA service template from URL (Docker Compose file, Service file, Python scripts)
    TOSCA Service Template is created based on the generated inputs.yaml file.
    """

    def __init__(self) -> None:
        # IO objects
        self.file_handler = FileHandler()
        self.network_handler = NetworkHandler()

        # Create inputs.yaml file
        host_list = self.file_handler.read_file(
            Configuration.HOST_FILE_PATH
        ).split("\n")

        input_file = InputsFile(host_list)
        input_file.build()
        input_yaml_file = input_file.export()

        self.file_handler.write_yaml_file(
            Configuration.INPUTS_YAML_FILE_PATH,
            input_yaml_file
        )

        # inputs name for the template creation
        self.input_names = list(input_yaml_file.keys())

    def create_service_template(self, url: str) -> None:
        "Create TOSCA Service Template from URL"

        services_yaml = self.network_handler.pull_yaml(url)

        tosca_service_template = ServiceTemplate(
            self.input_names,
            services_yaml
        )
        tosca_service_template.build()

        self.file_handler.write_yaml_file(
            Configuration.SERVICE_TEMPLATE_PATH,
            tosca_service_template.export()
        )


class NodeTypes:
    "All node types"

    COMPUTE = "tosca.nodes.Compute"

    SWARM_LEADER = "fog.docker.SwarmLeader"
    SWARM_WORKER = "fog.docker.SwarmWorker"

    DOCKER_SERVICE = "fog.docker.Services"

    DOCKER_CONTAINER = "fog.docker.Containers"
    SYSTEM_SERVICE = "fog.system.Service"


class YAMLBuilder(ABC):
    """
    Abstract for components of TOSCA YAML
    """

    def __init__(self) -> None:
        self.yaml = dict()

    @abstractmethod
    def build(self) -> None:
        "Build the YAML"
        pass

    def export(self) -> dict:
        "Returns created YAML"
        return self.yaml


class ServiceNode(YAMLBuilder):
    """
    Base class for fog service nodes
    """

    def __init__(self, host_node: str, dependency_nodes: list[str] = []) -> None:
        super().__init__()
        self.host_node = host_node
        self.dependency_nodes = dependency_nodes

    def build_requirements(self) -> list:
        "Builds the requirements of service nodes"

        requirements_list = [{"host": self.host_node}]

        for dependency_node in self.dependency_nodes:
            requirements_list.append({"dependency": dependency_node})

        return requirements_list


class Template(YAMLBuilder):
    """
    Base class for TOSCA Templates
    """

    def __init__(self, key: str) -> None:
        super().__init__()
        self.key = key

    def add_node(self, node: dict) -> None:
        "Adds component nodes into this template"

        for key in node.keys():
            self.yaml[self.key][key] = node[key]


class Generator:
    """
    Node name Generator
    """

    def __init__(self, prefix: str) -> None:
        self.prefix = prefix
        self.index = 0

    def generator(self):
        "Create Generator object"

        while True:
            self.index += 1
            yield f"{self.prefix}{self.index}"


class InputsFile(YAMLBuilder):
    """
    Build inputs.yaml file
    """

    def __init__(self, host_list: list[str]) -> None:
        super().__init__()

        self.host_list = host_list

    def build(self) -> None:
        node_name = Generator("node_").generator()

        for host in self.host_list:
            self.yaml[next(node_name)] = host


class Inputs(YAMLBuilder):
    """
    Builds inputs section for topology_templates
    """
    KEY = "inputs"

    def __init__(self, input_names: list[str]) -> None:
        super().__init__()
        self.input_names = input_names

    def build(self) -> None:
        self.yaml[Inputs.KEY] = dict()

        for name in self.input_names:
            self.yaml[Inputs.KEY][name] = {"type": "string"}


class Compute(YAMLBuilder):
    """
    Builds tosca.nodes.Compute nodes for node_templates
    """

    def __init__(self, node_name: str, host: str) -> None:
        super().__init__()
        self.host = host
        self.node_name = node_name

    def build(self) -> None:
        self.yaml[self.node_name] = {
            "type": "tosca.nodes.Compute",
            "attributes":
            {
                "private_address": {"get_input": self.host},
                "public_address": {"get_input": self.host}
            }
        }


class SwarmLeader(YAMLBuilder):
    """
    Builds fog.docker.SwarmLeader nodes for node_templates
    """

    def __init__(self, node_name: str, host_node: str) -> None:
        super().__init__()
        self.node_name = node_name
        self.host_node = host_node

    def build(self) -> None:
        self.yaml[self.node_name] = {
            "type": "fog.docker.SwarmLeader",
            "requirements":
            [
                {"host": self.host_node}
            ]
        }


class SwarmWorker(YAMLBuilder):
    """
    Builds fog.docker.SwarmWorker nodes for node_templates
    """

    def __init__(self, node_name: str, host_node: str, leader_node: str) -> None:
        super().__init__()
        self.node_name = node_name
        self.host_node = host_node
        self.leader_node = leader_node

    def build(self) -> None:
        self.yaml[self.node_name] = {
            "type": "fog.docker.SwarmWorker",
            "requirements":
            [
                {"host": self.host_node},
                {"leader": self.leader_node}
            ]
        }


class Outputs(YAMLBuilder):
    """
    Builds outputs section for service template
    """
    KEY = "outputs"

    def __init__(self, node_name: str) -> None:
        super().__init__()

        self.node_name = node_name

    def build(self) -> None:

        self.yaml[Outputs.KEY] = {
            "output_worker_token_attribute":
            {"value": {"get_attribute": [self.node_name, 'worker_token']}},
            "output_manager_token_attribute":
            {"value": {"get_attribute": [self.node_name, "manager_token"]}},
            "advertised_address":
            {"value": {"get_attribute": [self.node_name, "advertise_addr"]}}
        }


class Imports(YAMLBuilder):
    """
    Builds imports section for service template
    """

    KEY = "imports"

    import_index = {
        NodeTypes.SWARM_LEADER: "nodetypes/swarm_leader/swarm_leader.yaml",
        NodeTypes.SWARM_WORKER: "nodetypes/swarm_worker/swarm_worker.yaml",
        NodeTypes.DOCKER_SERVICE: "nodetypes/docker_services/docker_services.yaml",
        NodeTypes.DOCKER_CONTAINER: "nodetypes/docker_containers/docker_containers.yaml",
        NodeTypes.SYSTEM_SERVICE: "nodetypes/system_service/system_service.yaml"
    }

    def __init__(self, node_types: list[str]) -> None:
        super().__init__()

        self.node_types = node_types
        self.import_set = set()
        self.import_set.add(
            "relationshiptypes/token_transfer/token_transfer.yaml"
        )

    def build(self) -> None:
        for node_type in self.node_types:
            self.import_set.add(self.import_index[node_type])

        self.yaml[Imports.KEY] = list(self.import_set)


class DockerServices(ServiceNode):
    """
    Builds fog.docker.Services nodes for node_templates 
    """

    def __init__(
        self,
        node_name: str,
        service_name: str,
        url: str,
        host_node: str,
        dependency_nodes: list[str] = []
    ) -> None:
        super().__init__(host_node, dependency_nodes)

        self.node_name = node_name
        self.service_name = service_name
        self.url = url

    def build(self) -> None:
        self.yaml[self.node_name] = {
            "type": "fog.docker.Services",
            "properties":
            {
                "name": self.service_name,
                "url": self.url
            },
            "requirements": self.build_requirements()
        }


class DockerContainers(ServiceNode):
    """
    Builds fog.docker.Containers nodes for node_templates 
    """

    def __init__(
        self,
        node_name: str,
        compose_name: str,
        url: str,
        host_node: str,
        dependency_nodes: list[str] = [],
        packages: list[str] = []
    ) -> None:
        super().__init__(host_node, dependency_nodes)

        self.node_name = node_name
        self.compose_name = compose_name
        self.url = url
        self.packages = packages

    def build(self) -> None:
        self.yaml[self.node_name] = {
            "type": "fog.docker.Containers",
            "properties": {
                "name": self.compose_name,
                "url": self.url,
                "packages": [package for package in self.packages]
            },
            "requirements": self.build_requirements()
        }


class SystemService(ServiceNode):
    """
    Builds fog.system.Service nodes for node_templates 
    """

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
        super().__init__(host_node, dependency_nodes)

        self.node_name = node_name
        self.system_service_name = system_service_name
        self.script_url = script_url
        self.service_url = service_url
        self.packages = packages

    def build(self) -> None:
        self.yaml[self.node_name] = {
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


class NodeTemplates(Template):
    """
    Builds node_templates for topology_templates 
    """
    KEY = "node_templates"

    def __init__(self, hosts: list[str], services: dict) -> None:
        super().__init__(NodeTemplates.KEY)

        self.hosts = hosts
        self.services = services

        self.fog_nodes = []
        self.swarm_leader_name = "docker-swarm-leader"
        self.swarm_worker_names = []
        self.docker_service_name = "docker-service-1"

    def build_compute_nodes(self):
        compute_node_name = Generator("fog-node-").generator()
        for host in self.hosts:
            self.fog_nodes.append(next(compute_node_name))
            new_node = Compute(
                self.fog_nodes[-1],
                host
            )
            new_node.build()
            self.add_node(new_node.export())

    def build_docker_swarm_leader(self) -> None:
        new_node = SwarmLeader(self.swarm_leader_name, self.fog_nodes[0])
        new_node.build()
        self.add_node(new_node.export())

    def build_docker_swarm_worker(self) -> None:
        swarm_worker_name = Generator("docker-swarm-worker-").generator()

        for index, host in enumerate(self.fog_nodes):
            if index:
                self.swarm_worker_names.append(next(swarm_worker_name))
                new_node = SwarmWorker(
                    self.swarm_worker_names[-1],
                    host,
                    self.swarm_leader_name
                )
                new_node.build()
                self.add_node(new_node.export())

    def build_docker_services(self, url: str) -> None:
        docker_stack = Generator("docker_stack_").generator()

        new_node = DockerServices(
            self.docker_service_name,
            next(docker_stack),
            url,
            self.swarm_leader_name,
            self.swarm_worker_names
        )
        new_node.build()
        self.add_node(new_node.export())

    def build_docker_containers(
        self, url: str,
        dependency_packages: list[str]
    ) -> None:

        docker_container_node_name = Generator(
            "docker_container_node-").generator()
        docker_compose_name = next(Generator("docker_compose_").generator())

        for fog_node in self.fog_nodes:
            new_node = DockerContainers(
                next(docker_container_node_name),
                docker_compose_name,
                url,
                fog_node,
                [self.docker_service_name],
                dependency_packages
            )
            new_node.build()
            self.add_node(new_node.export())

    def build_system_service(
        self,
        name: str,
        script_url: str,
        service_url: str,
        dependency_packages: list[str]
    ) -> None:

        system_service_node_name = Generator(
            "system-service-").generator()

        for fog_node in self.fog_nodes:
            new_node = SystemService(
                next(system_service_node_name),
                name,
                script_url,
                service_url,
                fog_node,
                [self.docker_service_name],
                dependency_packages
            )
            new_node.build()
            self.add_node(new_node.export())

    def build(self) -> None:
        self.yaml[NodeTemplates.KEY] = dict()
        self.build_compute_nodes()

        self.build_docker_swarm_leader()
        self.build_docker_swarm_worker()

        for key in self.services.keys():
            match key:
                case NodeTypes.DOCKER_SERVICE:
                    self.build_docker_services(
                        self.services[NodeTypes.DOCKER_SERVICE]["url"]
                    )
                case NodeTypes.DOCKER_CONTAINER:
                    self.build_docker_containers(
                        self.services[NodeTypes.DOCKER_CONTAINER]["url"],
                        self.services[NodeTypes.DOCKER_CONTAINER]["dependency_packages"]
                    )
                case NodeTypes.SYSTEM_SERVICE:
                    self.build_system_service(
                        self.services[NodeTypes.SYSTEM_SERVICE]["name"],
                        self.services[NodeTypes.SYSTEM_SERVICE]["script_url"],
                        self.services[NodeTypes.SYSTEM_SERVICE]["service_url"],
                        self.services[NodeTypes.SYSTEM_SERVICE]["dependency_packages"]
                    )


class TopologyTemplate(Template):
    """
    Builds topology_template for service template
    """
    KEY = "topology_template"

    def __init__(self, input_names: list[str], services: dict) -> None:
        super().__init__(TopologyTemplate.KEY)

        self.input_names = input_names
        self.services = services

    def build_inputs(self) -> None:
        inputs = Inputs(self.input_names)
        inputs.build()
        self.add_node(inputs.export())

    def build_node_templates(self) -> None:
        node_templates = NodeTemplates(self.input_names, self.services)
        node_templates.build()
        self.add_node(node_templates.export())

    def build(self) -> None:
        self.yaml[TopologyTemplate.KEY] = dict()
        self.build_inputs()
        self.build_node_templates()


class ServiceTemplate(YAMLBuilder):
    """
    Builds TOSCA Service Templates
    """
    VERSION = "tosca_simple_yaml_1_3"

    def __init__(self, input_names: list[str], services: dict) -> None:
        super().__init__()

        self.input_names = input_names
        self.services = services

    def add_node(self, node: dict) -> None:
        for key in node.keys():
            self.yaml[key] = node[key]

    def build_version(self) -> None:
        self.yaml["tosca_definitions_version"] = ServiceTemplate.VERSION

    def build_imports(self) -> None:
        node_types = list(self.services.keys())
        node_types.append(NodeTypes.SWARM_LEADER)
        if len(self.input_names) > 1:
            node_types.append(NodeTypes.SWARM_WORKER)

        imports = Imports(node_types)
        imports.build()
        self.add_node(imports.export())

    def build_topology_template(self) -> None:
        topology_template = TopologyTemplate(self.input_names, self.services)
        topology_template.build()
        self.add_node(topology_template.export())

    def build(self) -> None:
        self.build_version()
        self.build_imports()
        self.build_topology_template()


if __name__ == "__main__":
    import yaml
    template = ServiceTemplate(
        ["node_1", "node_2"],
        {'fog.docker.Services':
         {'url': 'https://raw.githubusercontent.com/cloud-and-smart-labs/docker-images/main/websocket-led/docker-compose.yaml'},
         'fog.system.Service':
         {'name': 'led-websocket',
          'script_url': 'https://raw.githubusercontent.com/cloud-and-smart-labs/pi-system-service/master/led-websocket/led-websocket.py',
          'service_url': 'https://raw.githubusercontent.com/cloud-and-smart-labs/pi-system-service/master/led-websocket/led-websocket.service',
          'dependency_packages': ['websockets']
          }
         }
    )
    template.build()
    print(yaml.dump(template.export()))
