# harmony_commands.py
import subprocess
import asyncio

# Run the collect-rewards command and capture output
async def collect_rewards(address, hmy_app, gas_price, passphrase_file, harmony_validator_api):
    command = f"{hmy_app} staking collect-rewards --delegator-addr {address} --gas-price {gas_price} {passphrase_file} --node='{harmony_validator_api}'"
    process = await asyncio.create_subprocess_shell(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = await process.communicate()

    # Check if the command was successful
    if process.returncode == 0:
        return True
    else:
        print(f"Failed to collect rewards for address {address[:4]}...{address[-4:]}: {stderr.decode('utf-8')}")
        return False

# Run the transfer command and capture output
async def transfer_rewards(address, amount, hmy_app, gas_price, passphrase_file, harmony_validator_api, rewards_wallet):
    # Run the transfer command
    command = f"{hmy_app} transfer --amount {amount} --from {address} --from-shard 0 --to {rewards_wallet} --to-shard 0 --gas-price {gas_price} {passphrase_file} --node='{harmony_validator_api}'"
    output = await asyncio.create_subprocess_shell(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = await output.communicate()
    if output.returncode!= 0:
        print(f"Failed to transfer {amount} $ONE for address {address}: {stderr.decode('utf-8')}")
    else:
        return amount
    return 0