import asyncio
import websockets
import json
import subprocess
import shlex
import os
import sys


class ColorPrint:
    """
    Colored printing functions for strings that use universal ANSI escape sequences.
    fail: bold red, pass: bold green, warn: bold yellow,
    info: bold blue, bold: bold white
    """

    @staticmethod
    def print_fail(message, end="\n"):
        sys.stderr.write("\x1b[1;31m" + f"{message}" + "\x1b[0m" + end)

    @staticmethod
    def print_pass(message, end="\n"):
        sys.stdout.write("\x1b[1;32m" + f"{message}" + "\x1b[0m" + end)

    @staticmethod
    def print_warn(message, end="\n"):
        sys.stderr.write("\x1b[1;33m" + f"{message}" + "\x1b[0m" + end)

    @staticmethod
    def print_info(message, end="\n"):
        sys.stdout.write("\x1b[1;34m" + f"{message}" + "\x1b[0m" + end)

    @staticmethod
    def print_bold(message, end="\n"):
        sys.stdout.write("\x1b[1;37m" + f"{message}" + "\x1b[0m" + end)


def command_executor(cmd: str) -> dict:
    "Shell command executor"

    args = shlex.split(cmd)

    if len(args):
        try:
            shell_output = subprocess.run(args, capture_output=True,
                                          text=True)
            return {
                "cmd": cmd,
                "error_code": shell_output.returncode,
                "stdout": shell_output.stdout,
                "stderr": shell_output.stderr
            }

        except Exception as e:
            print(f"Exception (2): {str(e)}")

    return {
        "cmd": cmd,
        "error_code": "",
        "stdout": "",
        "stderr": ""
    }


async def client(host='localhost', port=80):
    "Websocket connection handler"

    async with websockets.connect(f'ws://{host}:{port}', ping_interval=None) as master:
        join = {
            "type": "orchestrator"
        }
        await master.send(json.dumps(join))
        ColorPrint.print_pass(" Connected ")

        while True:
            try:
                message = await master.recv()
                ColorPrint.print_pass("> ", end="")
                print(message)

                result = command_executor(message)
                await master.send(json.dumps(result))

                if "" != result["error_code"] and int(result["error_code"]):
                    print(result["stderr"])
                else:
                    print(result["stdout"])

            except websockets.ConnectionClosedOK:
                print('Connection closed')
                return
            except Exception as e:
                print(f"Exception (1): {e}")
                return


if __name__ == "__main__":

    # Default
    IP = 'localhost'
    PORT = 7890

    # env var
    if "IP" in os.environ:
        IP = os.environ["IP"]

    if "PORT" in os.environ:
        PORT = int(os.environ["PORT"])

    try:
        asyncio.run(client(host=IP, port=PORT))
    except KeyboardInterrupt as e:
        ColorPrint.print_fail("\n\n Terminate \n")
        exit(1)
