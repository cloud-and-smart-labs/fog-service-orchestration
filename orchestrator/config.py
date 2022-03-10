class Configuration:
    """
    Configuration file path and settings
    """

    @staticmethod
    def get_config_dir() -> str:
        return "/root/.config/"

    @staticmethod
    def get_host_file_path() -> str:
        return "/root/.config/HOST"

    @staticmethod
    def get_inputs_yaml_file_path() -> str:
        return "/root/tosca/inputs.yaml"
