import api.Client as Client
import subprocess
import sys
import time
import os

parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SERVER = os.path.join(parent_dir, 'api', 'Server.py')
CLIENT = os.path.join(parent_dir, 'api', 'Server.py')
EXPLAINER = os.path.join(parent_dir, 'explainer', 'ExplainerApp.py')
PRS = "systemTestSample.pptx"
python_path = sys.executable


def test_system():
    process1 = subprocess.Popen([python_path, SERVER])
    time.sleep(10)

    process2 = subprocess.Popen([python_path, EXPLAINER])
    time.sleep(10)

    uid = Client.upload(PRS)
    assert uid is not None, "Upload failed"

    status = Client.status(uid)
    print(status.status)
    assert status.status != "not found"

    time.sleep(100)
    status = Client.status(uid)
    print(status.status)
    assert status.status == "done"

    process1.kill()
    process2.kill()
