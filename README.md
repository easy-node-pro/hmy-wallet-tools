# rewards-collector
Our balance checker/rewards collector for any computer with wallets added to hmy application.  

## Setup
Assuming you already have python3 and pip installed, pull our github repo to your machine with hmy setup:  
`git clone https://github.com/easy-node-pro/hmy-wallet-tools.git`

Run setup of python dependencies:  
`pip3 install -r requirements.txt`

Then setup your .env file with your info. Set your paths for hmy, passphrase.txt, rewards wallet and if you'd like notifications when `python3 hmy_rewards.py -b` is run fill out an [ntfy.sh](ntfy.sh) link.  

### Wallet Password
Use the same password for all wallets and save it in a text file.  

### Acquiring hmy application
If you don't have hmy, after pulling the repo run the following:  

`wget harmony.one/hmy && chmod +x hmy`

Then install your keys into hmy. Use the help menu to figure it out:  

`./hmy keys --help`

### Using ntfy.sh for notifications
This is a simple notifications site. Pick any random url after ntfy.sh for example https://ntfy.sh/mycustomnotificationlinkisthebestone and use that as your url for notifications. Browse there and when you run the hmy_rewards.py app in collecting or balance mode you'll have an update sent to that url.  

## Using hmy-wallet-tools
Once you have everything setup, get your balance only notification by running (think of a cron job maybe?):  

`python3 hmy_rewards.py -b`