import asyncio
import websockets
import json


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
