import json
import aiohttp
import requests

# Helper function to send RPC requests
async def send_rpc_request(session, rpc_url, payload):
    headers = {'Content-Type': 'application/json'}
    async with session.post(rpc_url, headers=headers, data=json.dumps(payload)) as response:
        if response.status == 200:
            return await response.json()
        else:
            print(f"RPC request failed: {response.status}")
            print(f"Response: {await response.text()}")
            return None

# Get the balance of a wallet address using the Harmony RPC
async def get_balance(session, wallet_address, rpc_url):
    payload = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "hmyv2_getBalance",
        "params": [wallet_address]
    }
    response = await send_rpc_request(session, rpc_url, payload)
    if response:
        try:
            balance = int(response['result'])
            # Convert to ONE (1 ONE = 1e18 atto)
            return balance / 1e18
        except Exception as e:
            print(f"Failed to parse balance response for address {wallet_address[:4]}...{wallet_address[-4:]}: {e}")
    return None

# Get the pending rewards of a wallet address using the Harmony RPC
async def get_pending_rewards(session, address, harmony_rpc):
    payload = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "hmyv2_getDelegationsByDelegator",
        "params": [address]
    }
    response = await send_rpc_request(session, harmony_rpc, payload)
    if response:
        try:
            delegations = response['result']
            total_pending = sum(delegation['reward'] for delegation in delegations) / 1e18
            return total_pending
        except Exception as e:
            print(f"Failed to parse delegations response for address {address[:4]}...{address[-4:]}: {e}")
    return None

# Get the current price of Harmony (ONE) in USD from EasyNode
def get_harmony_price():
    url = "https://easynode.pro/api/price/harmony"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data["currentPriceInUSD"]
    else:
        print(f"Failed to get Harmony price. Status code: {response.status_code}")
        return None
