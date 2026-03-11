import os
import subprocess
import sys

def run_cmd(cmd):
    print(f"Running: {' '.join(cmd)}")
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.stdout:
        print(result.stdout)
    if result.stderr:
        print(result.stderr)
    return result.returncode

venv_dir = os.path.join(os.getcwd(), '.venv')
python_exe = os.path.join(venv_dir, 'Scripts', 'python.exe')

if not os.path.exists(python_exe):
    print(f"Python not found at {python_exe}")
    sys.exit(1)

# Try installing scipy
print("Attempting to install scipy...")
ret = run_cmd([python_exe, '-m', 'pip', 'install', 'scipy'])

if ret != 0:
    print("Pip install failed, trying to find pip...")
    # Maybe try to find where pip is
    pip_exe = os.path.join(venv_dir, 'Scripts', 'pip.exe')
    if os.path.exists(pip_exe):
        run_cmd([pip_exe, 'install', 'scipy'])
    else:
        print("pip.exe not found in Scripts")

# Check if it was installed
try:
    import scipy
    print("Scipy is now accessible in the current python (if this is the venv)")
except ImportError:
    print("Scipy is not accessible in the current python")
