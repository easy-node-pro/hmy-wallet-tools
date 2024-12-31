# harmony_wallets.py
import subprocess

# We will extract the list of addresses currently listed when running `./hmy keys list` in the terminal
def get_addresses(hmy_app):
    command = f"{hmy_app} keys list"
    output = subprocess.check_output(command, shell=True).decode('utf-8')
    lines = output.split('\n')
    addresses = []
    for line in lines[1:]:
        columns = line.split()
        if len(columns) > 1:
            address = columns[1]
            addresses.append(address)
    return addresses