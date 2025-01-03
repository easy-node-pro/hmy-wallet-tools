from os import environ
from dotenv import load_dotenv

class Config:
    def __init__(self):
        self.dotenv_file = "/home/serviceharmony/git/hmytb/.env"
        load_dotenv(self.dotenv_file)
        self.hmy_app = environ.get("HMY_APP")
        self.passphrase_file = environ.get("PASSPHRASE_FILE")
        self.rewards_wallet = environ.get("REWARDS_WALLET")
        self.harmony_validator_api = environ.get("HARMONY_VALIDATOR_API")
        self.harmony_rpc = environ.get("HARMONY_RPC")
        self.reserve_amount = float(environ.get("RESERVE_AMOUNT", 0))
        self.gas_price = environ.get("GAS_PRICE", 0)
        self.ntfy_url = environ.get("NTFY_URL")
        self.authorization_token = environ.get("AUTHORIZATION_TOKEN")
        
    def validate(self):
        """Validate the configuration"""
        essential_vars = [
            "hmy_app",
            "passphrase_file",
            "rewards_wallet",
            "harmony_validator_api",
            "harmony_rpc",
            "reserve_amount",
            "gas_price",
            "ntfy_url",
            "authorization_token"
        ]
        for var in essential_vars:
            if not getattr(self, var):
                raise ValueError(f"Config variable {var} is not set!")
            
config = Config()
config.validate()