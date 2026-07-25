import os
import subprocess
import sys

if __name__ == "__main__":
    command = [sys.executable, "-m", "streamlit", "run", "frontend/app.py"]
    subprocess.run(command, check=False)
