# harmony_wallets.py
import subprocess

# Get the list of wallet addresses
def get_addresses(hmy_app):
    try:
        command = f"{hmy_app} keys list"
        output = subprocess.check_output(command, shell=True).decode('utf-8')
        lines = output.split('\n')
        addresses = [line.split()[1] for line in lines[1:] if len(line.split()) > 1]
        return addresses
    except subprocess.CalledProcessError as e:
        print(f"Failed to list keys: {e}")
        return []
