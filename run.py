import os, sys, subprocess, venv, re

R = os.path.dirname(os.path.abspath(__file__))
V = os.path.join(R, ".venv")
P = os.path.join(V, "Scripts" if os.name=="nt" else "bin", "python")

def kill(port):
    if os.name == "nt":
        res = subprocess.run(f"netstat -ano | findstr :{port}", shell=True, capture_output=True, text=True)
        for pid in set(re.findall(r"\s(\d+)$", res.stdout, re.M)):
            if pid != "0": subprocess.run(f"taskkill /F /T /PID {pid}", shell=True, capture_output=True)

if sys.prefix != V:
    if not os.path.exists(V):
        print("> Creating venv...")
        venv.create(V, with_pip=True)
    subprocess.call([P, __file__] + sys.argv[1:])
    sys.exit()

print("\n--- BookGeek-AI ---")

print("Cleaning ports...")
for p in [8000, 5173]: kill(p)

print("Checking deps...")
subprocess.run([sys.executable, "-m", "pip", "install", "-q", "-r", "backend/requirements.txt"])

if not os.path.exists("frontend/node_modules"):
    print("Installing npm modules...")
    subprocess.run("npm install", cwd="frontend", shell=True)

if not os.path.exists("backend/app/models/cf_model.pkl"):
    if input("\nModels missing. Train? (y/N): ").lower() == 'y':
        subprocess.run([sys.executable, "app/train_models.py"], cwd="backend")

print("\nStarting...")
be = subprocess.Popen([sys.executable, "run.py", "--prod"], cwd="backend", shell=True)
fe = subprocess.Popen("npm run dev -- --host 127.0.0.1", cwd="frontend", shell=True)

print(f"Backend: http://127.0.0.1:8000\nFrontend: http://localhost:5173\n")

try:
    be.wait()
except KeyboardInterrupt:
    print("\nStopping...")
    for proc in [be, fe]:
        if os.name == "nt": subprocess.run(f"taskkill /F /T /PID {proc.pid}", capture_output=True)
        else: proc.terminate()

