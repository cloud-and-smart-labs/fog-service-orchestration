import asyncio
import websockets
import json
import shlex
import os
import time
from printer import ColorPrint
from command_executor import CommandExecutor
from tosca_processor import TOSCAProcessor


async def template_builder(url: str):
    "TOSCA Service Template creator"

    printer = ColorPrint()
    tosca = TOSCAProcessor()
    printer.log("Creating TOSCA Service Template")
    tosca.create_service_template(url)


async def shell_command_executor(type: str, command: str, master: websockets):
    "Shell command execute and send back the result"

    executor = CommandExecutor()
    printer = ColorPrint()

    # Command execution
    executor.set_command(command)
    printer.log("Command Executing")
    executor.execute()
    printer.log("Waiting for execution result")
    result = executor.result()
    printer.log("Got results")

    # Output view and send response
    result["type"] = type
    printer.output_viewer(result)

    await master.send(json.dumps(result))


async def command_handler(message: str, master: websockets):
    "Incoming command handler"

    printer = ColorPrint()

    json_msg = json.loads(message)

    if "cmd" == json_msg["type"]:
        printer.command_viewer(json_msg["cmd"])
        args = shlex.split(json_msg["cmd"])

        match args[0]:
            # TOSCA Template build command
            case "build":
                if 1 >= len(args):
                    printer.log("Missing URL")
                    return

                asyncio.create_task(template_builder(args[1]))

            # Cleanup with ansible-playbook
            case "cleanup":
                asyncio.create_task(shell_command_executor(
                    json_msg["type"],
                    "ansible-playbook cleanup.yaml",
                    master)
                )

            # Shell Command
            case _:
                asyncio.create_task(shell_command_executor(
                    json_msg["type"],
                    json_msg["cmd"],
                    master)
                )


async def client(host="localhost", port=80):
    "Websocket connection handler"

    async with websockets.connect(f"ws://{host}:{port}", ping_interval=None) as master:
        join = {
            "type": "orchestrator"
        }
        await master.send(json.dumps(join))
        ColorPrint.print_pass(" Connected ")

        while True:
            try:
                message = await master.recv()
                asyncio.create_task(command_handler(message, master))

            except websockets.ConnectionClosedOK:
                print("Connection closed")
                return
            except Exception as e:
                print(f"Exception:client: {e}")
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

    # Input file setup
    TOSCAProcessor()

    try:
        while True:
            try:
                asyncio.run(client(host=IP, port=PORT))
            except Exception as e:
                ColorPrint.print_fail(" Connection lost.")

                ColorPrint.print_info(" Trying to reconnect. \r", end="")
                time.sleep(1)
                ColorPrint.print_info(" Trying to reconnect.. \r", end="")
                time.sleep(1)
                ColorPrint.print_info(" Trying to reconnect... \r", end="")
                time.sleep(1)
                ColorPrint.print_info("                         \r", end="")

    except KeyboardInterrupt as e:
        ColorPrint.print_fail("\n\n Terminate \n")
        exit(1)
