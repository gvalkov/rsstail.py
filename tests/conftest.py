import subprocess
import pytest


@pytest.fixture
def rsstail():
    def inner(*args):
        cmd = ["python3", "-m", "rsstail", *args]
        ret = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd="./src")
        return ret
    return inner
