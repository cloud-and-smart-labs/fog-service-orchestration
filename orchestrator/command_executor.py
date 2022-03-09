import subprocess
import shlex


class CommandExecutor:
    """
    "Shell command executor"
    """

    def __init__(self) -> None:
        self._exception_flag = False

    def set_command(self, command: str) -> None:
        "Add command to execute"
        self._command = command
        args = shlex.split(self._command)
        if len(args):
            self.__command_args = args
        else:
            raise Exception("Command is empty!")

    def execute(self) -> None:
        "Execute added command"
        try:
            self.__shell_output = subprocess.run(self.__command_args,
                                                 capture_output=True,
                                                 text=True
                                                 )
        except Exception as e:
            self._exception_flag = True
            print(f"Exception (2): {str(e)}")

    def result(self) -> dict:
        "Get result after execution"
        if not self._exception_flag:
            return {
                "cmd": self._command,
                "error_code": self.__shell_output.returncode,
                "stdout": self.__shell_output.stdout,
                "stderr": self.__shell_output.stderr
            }
        else:
            return {
                "cmd": self._command,
                "error_code": "",
                "stdout": "",
                "stderr": ""
            }
