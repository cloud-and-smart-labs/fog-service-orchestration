import ssl
import yaml
from urllib.request import urlopen


class FileHandler:
    "File reader and writer"

    def read_file(self, file_path: str) -> str:
        "Read text file"
        with open(file_path) as file:
            content = file.read().strip()
            return content

    def write_file(self, file_path: str, content: str) -> None:
        "Write text file"
        with open(file_path, "w") as file:
            file.write(content)

    def write_yaml_file(self, file_path: str, content: dict) -> None:
        "Write YAML file"
        with open(file_path, "w") as file:
            file.write(yaml.dump(content))


class NetworkHandler():
    "Pull files from the internet"

    def __init__(self) -> None:
        self.context = ssl._create_unverified_context()

    def pull(self, url: str) -> str:
        "Pull as a text"
        with urlopen(url, context=self.context) as url:
            text = url.read().decode()
            return text

    def pull_yaml(self, url: str) -> dict:
        "Pull as a dict"
        return yaml.safe_load(self.pull(url))
