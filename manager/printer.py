import sys


class ColorPrint:
    """
    Colored printing functions for strings that use universal ANSI escape sequences.
    fail: bold red, pass: bold green, warn: bold yellow, 
    info: bold blue, bold: bold white
    """

    @staticmethod
    def print_fail(message: str, end="\n") -> None:
        sys.stderr.write("\x1b[1;31m" + f"{message}" + "\x1b[0m" + end)

    @staticmethod
    def print_pass(message: str, end="\n") -> None:
        sys.stdout.write("\x1b[1;32m" + f"{message}" + "\x1b[0m" + end)

    @staticmethod
    def print_warn(message: str, end="\n") -> None:
        sys.stderr.write("\x1b[1;33m" + f"{message}" + "\x1b[0m" + end)

    @staticmethod
    def print_info(message: str, end="\n") -> None:
        sys.stdout.write("\x1b[1;34m" + f"{message}" + "\x1b[0m" + end)

    @staticmethod
    def print_bold(message: str, end="\n") -> None:
        sys.stdout.write("\x1b[1;37m" + f"{message}" + "\x1b[0m" + end)

    def message_viewer(self, payload: list) -> None:
        "Command output viewer"
        for output in payload:
            self.hr_line()

            match output["type"]:
                case "cmd":
                    ColorPrint.print_pass("command", end=" : ")
                    print(output['cmd'])

                    ColorPrint.print_pass("error_code", end=" : ")
                    print(output["error_code"])

                    ColorPrint.print_pass("stdout", end=" : \n")
                    print(output["stdout"])

                    ColorPrint.print_pass("stderr", end=" : \n")
                    print(output["stderr"])

                case "admin":
                    ColorPrint.print_pass("cmd", end=" : ")
                    print(output['cmd'])

                    ColorPrint.print_pass("output", end=" : \n")
                    print(output["output"])

            self.hr_line()

    def info_viewer(self) -> None:
        "Starting details viewer"
        self.hr_line()
        ColorPrint.print_bold(" INFO")
        ColorPrint.print_pass(" Ctrl + C ", end="\t")
        ColorPrint.print_info(" Terminate ")

        ColorPrint.print_pass(" master count ", end="\t")
        ColorPrint.print_info(" Number of connected Orchestrators ")
        self.hr_line()

    def loader_start(self) -> None:
        "Loader"
        sys.stdout.write(" Starting... \r")

    def loader_stop(self) -> None:
        "Loader remove"
        sys.stdout.write("             \r")

    def hr_line(self) -> None:
        print("----------------------------------------------")
