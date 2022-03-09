import asyncio
import websockets
import multiprocessing
import json
import os
import shlex
from orchestration_manager import OrchestrationManager
from printer import ColorPrint


async def cli(host="localhost", port=80):
    "CLI for Orchestration Manager"

    def orchestration_manager() -> None:
        "Orchestration Manager starter"
        OrchestrationManager(port=port)

    # Starting OrchestrationManager Websocket server process
    server_process = multiprocessing.Process(target=orchestration_manager)
    server_process.start()

    printer = ColorPrint()

    printer.loader_start()
    await asyncio.sleep(2)
    printer.loader_stop()
    printer.info_viewer()

    # Starting CLI
    async with websockets.connect(f'ws://{host}:{port}', ping_interval=None) as websocket:

        async def send(msg: str) -> None:
            "Send message"
            try:
                await websocket.send(msg)
            except websockets.ConnectionClosedOK:
                print("Exception (1)")
            except Exception as e:
                print(f"Exception (2) : {e}")

        async def fetch() -> None:
            "Recevice message"

            try:
                await send(json.dumps({
                    "type": "fetch"
                }))

                message = await websocket.recv()
                json_msg = json.loads(message)

                if json_msg["payload"]:
                    printer.message_viewer(json_msg["payload"])

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
                        else:
                            ColorPrint.print_fail("Missing arg(s)")
                            continue
                    else:
                        request = {
                            "cmd": command,
                            "type": "cmd"
                        }
                    await send(json.dumps(request))

                await fetch()

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
