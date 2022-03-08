import asyncio
import websockets
import json
import multiprocessing
import shlex
import sys
import os


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


class OrchestrationManager:
    """
    Orchestration Manager manages all the orchestration nodes running behind NAT through Websockets
    """

    def __init__(self, host="0.0.0.0", port=80) -> None:
        self._HOST = host
        self._PORT = port
        self._cli_connection = None
        self._msg_queue = []
        self.__orchestrators = set()

        asyncio.run(self._server())

    async def _server(self) -> None:
        "Start Websockets server"
        async with websockets.serve(
            self._connection_handler,
            self._HOST,
            self._PORT,
            ping_interval=None,
        ):
            await asyncio.Future()

    async def _connection_handler(self, connection: websockets) -> None:
        "Manages authentication and connections"

        try:
            message = await connection.recv()
            connection_type = json.loads(message)

        except websockets.ConnectionClosedOK:
            print("_connection_handler : Connection closed")
            return
        except Exception as e:
            print(f"_connection_handler : {e}")
            await connection.close()
            return

        match connection_type["type"]:
            case "cli":
                self._cli_connection = connection
                await self._cli_connection_handler()

            case "orchestrator":
                self.__orchestrators.add(connection)
                await self._orchestrator_connection_handler(connection)

    async def _orchestrator_connection_handler(self, orchestrator_connection: websockets) -> None:
        "Orchestrator messages handler"

        try:
            async for output in orchestrator_connection:
                if self._cli_connection:
                    self._msg_queue.append(json.loads(output))

        except websockets.ConnectionClosedOK:
            print("_orchestrator_connection_handler : Connection closed")
        except Exception as e:
            print(f"_orchestrator_connection_handler : {e}")
        finally:
            self.__orchestrators.remove(orchestrator_connection)

    async def _cli_connection_handler(self) -> None:
        "CLI connection handler"

        try:
            async for message in self._cli_connection:
                json_msg = json.loads(message)

                match json_msg["type"]:
                    case "fetch":
                        if self._msg_queue:
                            json_msg["payload"] = self._msg_queue[:]
                            self._msg_queue.clear()

                        else:
                            json_msg["payload"] = []
                        await self._cli_connection.send((json.dumps(json_msg)))

                    case "cmd":
                        websockets.broadcast(self.__orchestrators, message)

                    case "admin":
                        json_msg["output"] = self._command_interpreter(
                            json_msg["cmd"])
                        self._msg_queue.append(json_msg)

        except websockets.ConnectionClosedOK:
            print("_cli_connection_handler : Connection closed")
        except Exception as e:
            print(f"_cli_connection_handler : {e}")
        finally:
            self._cli_connection = None

    def _command_interpreter(self, command: str) -> str:
        "Orchestration Manager management commands"

        match command:
            case "count":
                return str(len(self.__orchestrators))

            case _:
                return "INVALID"


async def cli(host="localhost", port=80):
    "CLI for Orchestration Manager"

    def orchestration_manager() -> None:
        "Orchestration Manager starter"
        OrchestrationManager(port=port)

    # Starting OrchestrationManager Websocket server process
    server_process = multiprocessing.Process(target=orchestration_manager)
    server_process.start()

    # Wait
    sys.stdout.write(" Starting... \r")
    await asyncio.sleep(2)
    sys.stdout.write("             \r")

    # Info
    print("----------------------------------------------")
    ColorPrint.print_bold(" INFO")
    ColorPrint.print_pass(" Ctrl + C ", end="\t")
    ColorPrint.print_info(" Terminate ")

    ColorPrint.print_pass(" master count ", end="\t")
    ColorPrint.print_info(" Number of connected Orchestrators ")
    print("----------------------------------------------")

    # Starting CLI
    async with websockets.connect(f'ws://{host}:{port}', ping_interval=None) as websocket:

        async def viewer(payload: list) -> None:
            for output in payload:
                print("-------------------------------------------")
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
                print("-------------------------------------------")

        async def send(msg: str) -> None:
            "Send message"
            try:
                await websocket.send(msg)
            except websockets.ConnectionClosedOK:
                print("Exception (1)")
            except Exception as e:
                print(f"Exception (2) : {e}")

        async def recv() -> None:
            "Recevice message"

            try:
                await send(json.dumps({
                    "type": "fetch"
                }))

                message = await websocket.recv()
                json_msg = json.loads(message)

                if json_msg["payload"]:
                    await viewer(json_msg["payload"])

            except websockets.ConnectionClosedOK:
                print("Exception (3)")
            except Exception as e:
                print(f"Exception (4) : {e}")

        await send(json.dumps({
            "type": "cli"
        }))

        while True:
            try:
                ColorPrint.print_pass("prompt", end=": ")
                command = input()

                if command:
                    args = shlex.split(command)

                    if "master" == args[0]:
                        if len(args) > 1:
                            request = {
                                "cmd": args[1],
                                "type": "admin"
                            }
                            await send(json.dumps(request))
                        else:
                            ColorPrint.print_fail("Missing arg(s)")

                    else:
                        request = {
                            "cmd": command,
                            "type": "cmd"
                        }
                        await send(json.dumps(request))

                await recv()

            except KeyboardInterrupt:
                ColorPrint.print_fail("\n\n Terminate \n")
                server_process.terminate()
                exit(1)


if __name__ == "__main__":

    # Default
    PORT = 7890

    # env var
    if "PORT" in os.environ:
        PORT = int(os.environ["PORT"])

    asyncio.run(cli(port=PORT))
