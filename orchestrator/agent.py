import asyncio
import websockets
import json
import shlex
import os
from printer import ColorPrint
from command_executor import CommandExecutor
from tosca_processor import TOSCAProcessor


async def client(host="localhost", port=80):
    "Websocket connection handler"

    tosca = TOSCAProcessor()
    printer = ColorPrint()
    executor = CommandExecutor()

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

                        args = shlex.split(json_msg["cmd"])

                        # TOSCA Template build command
                        if "build" == args[0]:
                            tosca.create_service_template(args[1])

                        # Shell Command
                        else:
                            executor.set_command(json_msg["cmd"])
                            printer.log("Command Executing")
                            executor.execute()
                            printer.log("Waiting for execution result")
                            result = executor.result()
                            printer.log("Got results")

                            # Output view and send response
                            result["type"] = json_msg["type"]
                            printer.output_viewer(result)

                            await master.send(json.dumps(result))

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
