import subprocess
import shlex


class CommandExecutor:
    """
    Shell command executor
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
            self.__shell_output = subprocess.run(
                self.__command_args,
                capture_output=True,
                text=True
            )

        except Exception as e:
            self._exception_flag = True
            print(f"Exception (2): {str(e)}")

    def result(self) -> dict:
        "Get result after execution"

        if not self._exception_flag:
            return CommandExecutor.output_format(
                self._command,
                self.__shell_output.returncode,
                self.__shell_output.stdout,
                self.__shell_output.stderr
            )
        else:
            return CommandExecutor.output_format(
                self._command, "", "", ""
            )

    @staticmethod
    def output_format(
        cmd: str,
        error_code: int,
        stdout: str,
        stderr: str
    ) -> dict:
        return {
            "cmd": cmd,
            "error_code": error_code,
            "stdout": stdout,
            "stderr": stderr
        }
