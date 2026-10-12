import os
import subprocess
import sys
import time
from arduino.app_utils import App

WEB_APP = "/app/web_app.py"

def loop():
    print("TOUCHGRASS - BIRD EXPLORER", flush=True)
    print("Starting phone upload server...", flush=True)

    if not os.path.isfile(WEB_APP):
        print("ERROR: web_app.py not found!", flush=True)
        return

    server = subprocess.Popen(
        [sys.executable, WEB_APP],
        cwd="/app"
    )

    try:
        while server.poll() is None:
            time.sleep(2)
        print("Web server exited:", server.returncode, flush=True)
    finally:
        if server.poll() is None:
            server.terminate()
            server.wait()

App.run(user_loop=loop)
