import asyncio
import websockets
import json
import multiprocessing
import shlex


class OrchestrationManager:
    def __init__(self, host='0.0.0.0', port=80) -> None:
        self._HOST = host
        self._PORT = port
        self.__orchestrators = set()
        self._cli_connection = None

        asyncio.run(self._server())

    async def _server(self) -> None:
        async with websockets.serve(
            self._connection_handler,
            self._HOST,
            self._PORT,
            ping_interval=None,
        ):
            await asyncio.Future()

    async def _connection_handler(self, connection) -> None:
        try:
            message = await connection.recv()
        except websockets.ConnectionClosedOK:
            # print('_connection_handler : Connection closed')
            return
        except Exception as e:
            # print(f'_connection_handler : {e}')
            return

        connection_type = json.loads(message)
        # print(connection_type)

        if 'cli' == connection_type['type']:
            self._cli_connection = connection
            await self._cli_connection_handler()

        elif 'orchestrator' == connection_type['type']:
            self.__orchestrators.add(connection)
            await self._orchestrator_connection_handler(connection)

    async def _orchestrator_connection_handler(self, orchestrator_connection) -> None:
        try:
            async for output in orchestrator_connection:
                # print(f'ORCH: {output}')
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
                            self.command_interpreter(json_msg["cmd"])
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

    def command_interpreter(self, command):
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
    def orchestration_manager():
        OrchestrationManager(port=port)
    server_process = multiprocessing.Process(target=orchestration_manager)
    server_process.start()
    # await asyncio.sleep(1)

    async with websockets.connect(f'ws://{host}:{port}', ping_interval=None) as websocket:

        async def send(websocket, msg):
            try:
                await websocket.send(msg)
            except websockets.ConnectionClosedOK:
                print('Connection closed')
            except Exception as e:
                print(f'Exception (1) : {e}')

        async def recv(websocket):
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
        await send(websocket, json.dumps(join))

        async def command_output(request):
            await send(websocket, request)
            orch = int(await recv(websocket))
            for i in range(orch):
                print(f'NAT {i}')
                json_msg = json.loads(await recv(websocket))

                print(f"command: {json_msg['cmd']}")
                print(f"error_code: {json_msg['error_code']}")
                print(f"stdout: \n{json_msg['stdout']}")
                print(f"stderr: \n{json_msg['stderr']}\n")

        async def management_output(request):
            await send(websocket, request)
            json_msg = json.loads(await recv(websocket))

            print(f"command: {json_msg['cmd']}")
            print(f"output: {json_msg['output']}")

        while True:
            try:
                command = input("prompt: ")
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
                print('\n\n Terminate. \n')
                server_process.terminate()
                exit(1)


if __name__ == '__main__':
    asyncio.run(cli(port=7890))
