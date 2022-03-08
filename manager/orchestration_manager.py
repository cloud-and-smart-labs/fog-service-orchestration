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

    def __init__(self, host='0.0.0.0', port=80) -> None:
        self._HOST = host
        self._PORT = port
        self.__orchestrators = set()
        self._cli_connection = None

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
            # print(connection_type)

        except websockets.ConnectionClosedOK:
            # print('_connection_handler : Connection closed')
            return
        except Exception as e:
            # print(f'_connection_handler : {e}')
            await connection.close()
            return

        if 'cli' == connection_type['type']:
            self._cli_connection = connection
            await self._cli_connection_handler()

        elif 'orchestrator' == connection_type['type']:
            self.__orchestrators.add(connection)
            await self._orchestrator_connection_handler(connection)

    async def _orchestrator_connection_handler(self, orchestrator_connection: websockets) -> None:
        "Orchestrator messages handler"
        try:
            async for output in orchestrator_connection:
                # print(f'ORCH: {output}')
                if self._cli_connection:
                    await self._cli_connection.send(output)
        except websockets.ConnectionClosedOK:
            pass
            # print('_orchestrator_connection_handler : Connection closed')
        except Exception as e:
            pass
            # print(f'_orchestrator_connection_handler : {e}')
        finally:
            self.__orchestrators.remove(orchestrator_connection)

    async def _cli_connection_handler(self) -> None:
        "CLI connection handler"
        try:
            async for message in self._cli_connection:
                # print(f'CLI: {cmd}')
                json_msg = json.loads(message)
                # print(json_msg)

                if "cmd" == json_msg["type"]:
                    await self._cli_connection.send(str(len(self.__orchestrators)))
                    websockets.broadcast(self.__orchestrators, json_msg["cmd"])

                elif "admin" == json_msg["type"]:
                    await self._cli_connection.send(
                        json.dumps(
                            self._command_interpreter(json_msg["cmd"])
                        )
                    )

        except websockets.ConnectionClosedOK:
            pass
            # print('_cli_connection_handler : Connection closed')
        except Exception as e:
            pass
            # print(f'_cli_connection_handler : {e}')
        finally:
            self._cli_connection = None

    def _command_interpreter(self, command: str) -> dict:
        "Orchestration Manager management commands"

        response = {
            "cmd": command
        }

        match command:
            case 'count':
                response["output"] = len(self.__orchestrators)
                return response
            case _:
                response["output"] = "INVALID"
                return response


async def cli(host='localhost', port=80):
    "CLI for Orchestration Manager"

    def orchestration_manager() -> None:
        "Orchestration Manager starter"
        OrchestrationManager(port=port)

    # Starting OrchestrationManager Websocket server process
    server_process = multiprocessing.Process(target=orchestration_manager)
    server_process.start()
    # await asyncio.sleep(1)

    # Starting CLI
    async with websockets.connect(f'ws://{host}:{port}', ping_interval=None) as websocket:

        async def send(msg: str) -> str:
            "Send message"
            try:
                await websocket.send(msg)
            except websockets.ConnectionClosedOK:
                print('Connection closed')
            except Exception as e:
                print(f'Exception (1) : {e}')

        async def recv() -> str:
            "Recevice message"
            msg = None
            try:
                msg = await websocket.recv()
            except websockets.ConnectionClosedOK:
                print('Connection closed')
            except Exception as e:
                print(f'Exception (2) : {e}')
            finally:
                return msg

        join = {
            "type": "cli"
        }
        await send(json.dumps(join))

        async def command_output(request: str) -> None:
            "Command for connected orchestrators"

            await send(request)
            orch = int(await recv())

            for i in range(orch):
                ColorPrint.print_warn(f' | NAT {i} | ')

                json_msg = json.loads(await recv())

                ColorPrint.print_pass("command", end=" : ")
                ColorPrint.print_info(json_msg['cmd'])

                ColorPrint.print_pass("error_code", end=" : ")
                ColorPrint.print_info(json_msg["error_code"])

                ColorPrint.print_pass("stdout", end=" : \n")
                ColorPrint.print_info(json_msg["stdout"])

                ColorPrint.print_pass("stderr", end=" : \n")
                ColorPrint.print_info(json_msg["stderr"])

        async def management_output(request: str) -> None:
            "Command for connected orchestration manager"
            await send(request)
            json_msg = json.loads(await recv())

            # print(f"command: {json_msg['cmd']}")
            ColorPrint.print_pass("command", end=" : ")
            ColorPrint.print_info(json_msg['cmd'])

            ColorPrint.print_pass("output", end=" : \n")
            ColorPrint.print_info(json_msg["output"])

        while True:
            try:
                ColorPrint.print_pass("prompt", end=": ")
                command = input()
                args = shlex.split(command)

                if "master" == args[0] and len(args) > 1:
                    request = {
                        "cmd": args[1],
                        "type": "admin"
                    }
                    await management_output(json.dumps(request))

                else:
                    request = {
                        "cmd": command,
                        "type": "cmd"
                    }
                    await command_output(json.dumps(request))

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
