import subprocess

steam_command = 'steam://friends/status/away'

try:
    subprocess.run(['start', steam_command], check=True, shell=True)
except subprocess.CalledProcessError as e:
    print(f"Error running Steam command: {e}")
