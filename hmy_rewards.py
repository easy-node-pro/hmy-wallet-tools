import aiohttp
import asyncio
import argparse
from harmony_utils import harmony_client, harmony_commands, harmony_notifications, harmony_wallets
from harmony_utils.config import config
from harmony_utils.animals import get_random_animal_emoji

async def main():
    addresses = harmony_wallets.get_addresses(config.hmy_app)
    parser = argparse.ArgumentParser(description="Get balance and pending rewards")
    parser.add_argument("-b", "--balance", action="store_true", help="Show balance and pending rewards")
    args = parser.parse_args()
    total_pending = 0
    notification_message = ""
    address_rewards = []  # List to store (address, balance, pending_rewards)
    total_transferred = 0
    
    async with aiohttp.ClientSession() as session:
        # Run the get-balance and get-pending-rewards commands for each address
        for address in addresses:
            # Get balance
            balance = await harmony_client.get_balance(session, address, config.harmony_rpc)
            if balance is None:
                continue

            # Get pending rewards
            pending_rewards = await harmony_client.get_pending_rewards(session, address, config.harmony_rpc)
            if pending_rewards is None:
                continue

            address_rewards.append((address, balance, pending_rewards))
            total_pending += pending_rewards

        # Sort addresses based on pending rewards in descending order
        address_rewards.sort(key=lambda x: x[2], reverse=True)
        
        if args.balance:
            for address, balance, pending_rewards in address_rewards:
                notification_message += f"{get_random_animal_emoji()}: {address[:4]}...{address[-4:]}, Balance: {round(balance, 2)} ONE, Pending Rewards: {round(pending_rewards, 2)} ONE\n"
            price = harmony_client.get_harmony_price()
            notification_message += f"\nTotal pending rewards: {round(total_pending, 4)} $ONE 💲{round(total_pending * price, 2)} USD"
            harmony_notifications.send_notification(config.ntfy_url, notification_message, "Harmony Balance Notification", "moneybag,harmony,rewards,balances", "default", config.authorization_token)
        
        else:
            # Run the collect-rewards, get-balance, and transfer commands for each address
            for address, balance, pending_rewards in address_rewards:
                # Collect rewards
                task = asyncio.create_task(harmony_commands.collect_rewards(address, config.hmy_app, config.gas_price, config.passphrase_file, config.harmony_validator_api))
                collected = await task
                if not collected:
                    continue

                # Get balance
                task = asyncio.create_task(harmony_client.get_balance(session, address, config.harmony_rpc))
                balance = await task
                if balance is None:
                    continue
                
                # Get current price of $ONE
                price = harmony_client.get_harmony_price()

                # Calculate transfer amount
                transfer_amount = max(0, float(balance) - config.reserve_amount)

                # Transfer rewards
                if transfer_amount > 0:
                    amount_transferred = await harmony_commands.transfer_rewards(address, transfer_amount, config.hmy_app, config.gas_price, config.passphrase_file, config.harmony_validator_api, config.rewards_wallet)
                    notification_message += f"Transferred {round(amount_transferred, 4)} $ONE to {address[:4]}...{address[-4:]}.\n"
                    total_transferred += amount_transferred
                else:
                    print(f"Not enough rewards to transfer for address {address[:4]}...{address[-4:]}")

            notification_message += f"\nTotal rewards transferred: {round(total_pending, 4)} $ONE 💲{round(total_pending * price, 2)} USD"
            harmony_notifications.send_notification(config.ntfy_url, notification_message, "Harmony Rewards Notification", "red_circle,harmony,rewards,claimed", "high", config.authorization_token)

if __name__ == "__main__":
    asyncio.run(main())
