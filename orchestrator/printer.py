import sys


class ColorPrint:
    """
    Colored printing functions for strings that use universal ANSI escape sequences.
    fail: bold red, pass: bold green, warn: bold yellow,
    info: bold blue, bold: bold white
    """

    @staticmethod
    def print_fail(message: str, end="\n"):
        sys.stderr.write("\x1b[1;31m" + f"{message}" + "\x1b[0m" + end)

    @staticmethod
    def print_pass(message: str, end="\n"):
        sys.stdout.write("\x1b[1;32m" + f"{message}" + "\x1b[0m" + end)

    @staticmethod
    def print_warn(message: str, end="\n"):
        sys.stderr.write("\x1b[1;33m" + f"{message}" + "\x1b[0m" + end)

    @staticmethod
    def print_info(message: str, end="\n"):
        sys.stdout.write("\x1b[1;34m" + f"{message}" + "\x1b[0m" + end)

    @staticmethod
    def print_bold(message: str, end="\n"):
        sys.stdout.write("\x1b[1;37m" + f"{message}" + "\x1b[0m" + end)

    def log(self, log_msg: str) -> None:
        ColorPrint.print_warn(f"+ {log_msg}")

    def command_viewer(self, command: str) -> None:
        "Command to be executed"
        ColorPrint.print_pass("> ", end="")
        print(command)

    def output_viewer(self, output: dict) -> None:
        "Output of the executed command"
        for line in output["stdout"].split("\n"):
            ColorPrint.print_info("< ", end="")
            print(line)
        for line in output["stderr"].split("\n"):
            ColorPrint.print_fail("< ", end="")
            print(line)


if __name__ == "__main__":
    ColorPrint.print_fail("Fail")
    ColorPrint.print_pass("Pass")
    ColorPrint.print_warn("Warn")
    ColorPrint.print_info("Info")
    ColorPrint.print_bold("Bold")
