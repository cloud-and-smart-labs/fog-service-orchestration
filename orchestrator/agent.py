import asyncio
import websockets
import json
import os
from printer import ColorPrint
from command_executor import CommandExecutor
from tosca_processor import TOSCAProcessor


async def client(host="localhost", port=80):
    "Websocket connection handler"

    tosca = TOSCAProcessor()
    printer = ColorPrint()

    async with websockets.connect(f"ws://{host}:{port}", ping_interval=None) as master:
        join = {
            "type": "orchestrator"
        }
        await master.send(json.dumps(join))
        ColorPrint.print_pass(" Connected ")

        while True:
            try:
                message = await master.recv()
                json_msg = json.loads(message)

                match json_msg["type"]:
                    case "cmd":
                        printer.command_viewer(json_msg["cmd"])

                        executor = CommandExecutor()
                        executor.set_command(json_msg["cmd"])
                        executor.execute()
                        result = executor.result()

                        result["type"] = json_msg["type"]

                        await master.send(json.dumps(result))

                        printer.output_viewer(result)

            except websockets.ConnectionClosedOK:
                print("Connection closed")
                return
            except Exception as e:
                print(f"Exception (1): {e}")
                return


if __name__ == "__main__":

    # Default
    IP = "localhost"
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
