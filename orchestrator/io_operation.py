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


class Network():
    def __init__(self) -> None:
        self.context = ssl._create_unverified_context()

    def fetch(self, url: str) -> str:
        with urlopen(url, context=self.context) as url:
            data = url.read().decode()
            return data
