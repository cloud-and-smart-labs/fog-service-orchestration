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
            if line:
                ColorPrint.print_info("< ", end="")
                print(line)
        for line in output["stderr"].split("\n"):
            if line:
                ColorPrint.print_fail("< ", end="")
                print(line)


if __name__ == "__main__":
    ColorPrint.print_fail("Fail")
    ColorPrint.print_pass("Pass")
    ColorPrint.print_warn("Warn")
    ColorPrint.print_info("Info")
    ColorPrint.print_bold("Bold")

    test_dict = {'cmd': 'ls -l',
                 'error_code': 0,
                 'stderr': '',
                 'stdout': 'total 56\n'
                 '-rw-r--r--   1 suvambasak  staff  11357  7 Mar 20:48 LICENSE\n'
                 '-rw-r--r--   1 suvambasak  staff   7804  7 Mar 20:48 README.md\n'
                 '-rw-r--r--   1 suvambasak  staff    272 13 Mar 13:44 '
                 'docker-compose.yaml\n'
                 'drwxr-xr-x   4 suvambasak  staff    128  7 Mar 20:48 docs\n'
                 'drwxr-xr-x   7 suvambasak  staff    224 13 Mar 08:48 manager\n'
                 'drwxr-xr-x  12 suvambasak  staff    384 13 Mar 13:54 orchestrator\n'
                 '-rw-r--r--   1 suvambasak  staff    209  7 Mar 20:48 '
                 'requirements.txt\n'}

    printer = ColorPrint()
    print(printer.output_viewer(test_dict))
