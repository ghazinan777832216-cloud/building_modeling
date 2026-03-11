import subprocess
import sys
import os

venv_python = os.path.join(os.getcwd(), '.venv', 'Scripts', 'python.exe')
print(f"Using venv python: {venv_python}")

try:
    subprocess.check_call([venv_python, '-m', 'pip', 'install', 'scipy'])
    print("Scipy installed successfully")
except Exception as e:
    print(f"Error installing scipy: {e}")
    sys.exit(1)
