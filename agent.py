import asyncio
import websockets
import json
import subprocess
import shlex


def command_executor(cmd):
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
            print(str(e))
    return {
        "cmd": cmd,
        "error_code": "",
        "stdout": "",
        "stderr": ""
    }


async def client(host='localhost', port=80):
    async with websockets.connect(f'ws://{host}:{port}', ping_interval=None) as master:
        join = {
            "type": "orchestrator"
        }
        await master.send(json.dumps(join))
        while True:
            try:
                message = await master.recv()
                print(message)
                result = command_executor(message)
                await master.send(json.dumps(result))
            except websockets.ConnectionClosedOK:
                print('Connection closed')
                return
            except Exception as e:
                print(f'Exception : {e}')
                return

host = 'localhost'
port = 7890
asyncio.run(client(host=host, port=port))
