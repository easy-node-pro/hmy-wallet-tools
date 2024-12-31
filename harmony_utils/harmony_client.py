# harmony_client.py
import json
import requests

# Get the balance of a wallet address using the Harmony RPC
async def get_balance(session, wallet_address, rpc_url):
    payload = json.dumps({
      "jsonrpc": "2.0",
      "id": 1,
      "method": "hmyv2_getBalance",
      "params": [
        wallet_address
      ]
    })
    headers = {
      'Content-Type': 'application/json'
    }

    async with session.post(rpc_url, headers=headers, data=payload) as response:
        if response.status == 200:
            try:
                balance_response = await response.json()
                balance = balance_response['result']
                # Convert to ONE (1 ONE = 1e18 atto)
                balance_in_one = balance / 1e18
                return balance_in_one
            except Exception as e:
                print(f"Failed to parse balance response for address {wallet_address[:4]}...{wallet_address[-4:]}: {e}")
                print(f"Response: {await response.text()}")
                return None
        else:
            print(f"Failed to get balance for address {wallet_address[:4]}...{wallet_address[-4:]}: {response.status}")
            print(f"Response: {await response.text()}")
            return None

# Get the pending rewards of a wallet address using the Harmony RPC
async def get_pending_rewards(session, address, harmony_rpc):
    payload = json.dumps({
      "jsonrpc": "2.0",
      "id": 1,
      "method": "hmyv2_getDelegationsByDelegator",
      "params": [
        address
      ]
    })
    headers = {
      'Content-Type': 'application/json'
    }

    async with session.post(harmony_rpc, headers=headers, data=payload) as response:
        if response.status == 200:
            try:
                delegations_response = await response.json()
                delegations = delegations_response['result']
                total_pending = 0
                for delegation in delegations:
                    total_pending += delegation['reward'] / 1e18
                return total_pending
            except Exception as e:
                print(f"Failed to parse delegations response for address {address[:4]}...{address[-4:]}: {e}")
                print(f"Response: {await response.text()}")
                return None
        else:
            print(f"Failed to get delegations for address {address[:4]}...{address[-4:]}: {response.status}")
            print(f"Response: {await response.text()}")
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
