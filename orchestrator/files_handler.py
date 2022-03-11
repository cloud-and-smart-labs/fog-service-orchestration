import yaml


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
