# harmony_commands.py
import subprocess
import asyncio

# Helper function to run shell commands asynchronously
async def run_shell_command(command):
    process = await asyncio.create_subprocess_shell(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = await process.communicate()
    return process.returncode, stdout.decode(), stderr.decode()

# Run the collect-rewards command and capture output
async def collect_rewards(address, hmy_app, gas_price, passphrase_file, harmony_validator_api):
    command = f"{hmy_app} staking collect-rewards --delegator-addr {address} --gas-price {gas_price} {passphrase_file} --node='{harmony_validator_api}'"
    returncode, stdout, stderr = await run_shell_command(command)
    if returncode == 0:
        return True
    else:
        print(f"Failed to collect rewards: {stderr}")
        return False

# Run the transfer command and capture output
async def transfer_rewards(address, amount, hmy_app, gas_price, passphrase_file, harmony_validator_api, rewards_wallet):
    command = f"{hmy_app} transfer --amount {amount} --from {address} --from-shard 0 --to {rewards_wallet} --to-shard 0 --gas-price {gas_price} {passphrase_file} --node='{harmony_validator_api}'"
    returncode, stdout, stderr = await run_shell_command(command)
    if returncode == 0:
        return amount
    else:
        print(f"Failed to transfer rewards: {stderr}")
        return 0
