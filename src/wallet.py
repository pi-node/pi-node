import os
import json
import logging
import requests
import asyncio
from Crypto.PublicKey import RSA
from Crypto.Hash import SHA256
from Crypto.Signature import pkcs1_15
from dotenv import load_dotenv
from datetime import datetime

# Load environment variables
load_dotenv()

# Load configuration from config.py
from config import (
    EXTERNAL_API_URL,
    TRANSACTION_FEE,
    LOG_LEVEL,
)

# Configure logging
logging.basicConfig(level=LOG_LEVEL, format='%(asctime)s - %(levelname)s - %(message)s')

class PiWallet:
    def __init__(self):
        self.api_url = EXTERNAL_API_URL
        self.wallet = {
            'address': None,
            'private_key': None,
            'balance': 0,
            'transaction_history': []
        }

    def generate_wallet(self):
        key = RSA.generate(2048)
        self.wallet['private_key'] = key.export_key()
        self.wallet['address'] = self.get_address_from_private_key(self.wallet['private_key'])
        logging.info(f'New wallet created: Address: {self.wallet["address"]}')
        self.save_wallet()

    def save_wallet(self):
        with open('wallet.json', 'w') as f:
            json.dump({
                'address': self.wallet['address'],
                'private_key': self.wallet['private_key'].decode('utf-8')
            }, f, indent=2)
        logging.info('Wallet saved to wallet.json')

    def load_wallet(self):
        if os.path.exists('wallet.json'):
            with open('wallet.json', 'r') as f:
                wallet_data = json.load(f)
                self.wallet['address'] = wallet_data['address']
                self.wallet['private_key'] = wallet_data['private_key'].encode('utf-8')
                logging.info(f'Wallet loaded: Address: {self.wallet["address"]}')
        else:
            logging.error('No wallet found. Please create a new wallet.')

    def get_address_from_private_key(self, private_key):
        key = RSA.import_key(private_key)
        public_key = key.publickey()
        return SHA256.new(public_key.export_key()).hexdigest()[:42]  # Simplified address generation

    async def check_balance(self):
        try:
            response = await asyncio.to_thread(requests.get, f'{self.api_url}/balance/{self.wallet["address"]}')
            self.wallet['balance'] = response.json().get('balance', 0)
            logging.info(f'Balance for {self.wallet["address"]}: {self.wallet["balance"]} Pi')
        except Exception as e:
            logging.error(f'Error checking balance: {e}')

    async def send_coins(self, to_address, amount):
        if amount > self.wallet['balance']:
            logging.error('Insufficient balance')
            return

        transaction = {
            'from': self.wallet['address'],
            'to': to_address,
            'amount': amount,
            'timestamp': int(datetime.now().timestamp())
        }

        # Sign the transaction
        key = RSA.import_key(self.wallet['private_key'])
        signature = pkcs1_15.new(key).sign(SHA256.new(json.dumps(transaction).encode('utf-8')))
        transaction['signature'] = signature.hex()

        try:
            response = await asyncio.to_thread(requests.post, f'{self.api_url}/send', json=transaction)
            if response.status_code == 200:
                logging.info(f'Transaction successful: {response.json().get("transactionId")}')
                self.wallet['balance'] -= amount  # Update local balance
                transaction['status'] = 'sent'
                self.wallet['transaction_history'].append(transaction)  # Log transaction
            else:
                logging.error(f'Error sending coins: {response.text}')
        except Exception as e:
            logging.error(f'Error sending coins: {e}')

    def display_wallet_info(self):
        logging.info('Wallet Information:')
        logging.info(f'Address: {self.wallet["address"]}')
        logging.info(f'Balance: {self.wallet["balance"]} Pi')
        logging.info('Transaction History:')
        for tx in self.wallet['transaction_history']:
            logging.info(f'Transaction: {tx}')

    def backup_wallet(self):
        backup_file = f'wallet_backup_{self.wallet["address"]}.json'
        with open(backup_file, 'w') as f:
            json.dump(self.wallet, f, indent =2)
        logging.info(f'Wallet backed up to {backup_file}')

    def restore_wallet(self, backup_file):
        if os.path.exists(backup_file):
            with open(backup_file, 'r') as f:
                wallet_data = json.load(f)
                self.wallet = wallet_data
                logging.info(f'Wallet restored from {backup_file}')
        else:
            logging.error('Backup file not found.')

# Command-line interface for user interaction
async def main():
    import argparse

    parser = argparse.ArgumentParser(description='Pi Wallet CLI')
    parser.add_argument('command', choices=['create', 'load', 'balance', 'send', 'info', 'backup', 'restore'], help='Command to execute')
    parser.add_argument('--to', type=str, help='Recipient address for sending coins')
    parser.add_argument('--amount', type=float, help='Amount of coins to send')
    parser.add_argument('--backup_file', type=str, help='Backup file to restore from')

    args = parser.parse_args()
    wallet = PiWallet()

    if args.command == 'create':
        wallet.generate_wallet()
    elif args.command == 'load':
        wallet.load_wallet()
    elif args.command == 'balance':
        await wallet.check_balance()
    elif args.command == 'send' and args.to and args.amount:
        await wallet.send_coins(args.to, args.amount)
    elif args.command == 'info':
        wallet.display_wallet_info()
    elif args.command == 'backup':
        wallet.backup_wallet()
    elif args.command == 'restore' and args.backup_file:
        wallet.restore_wallet(args.backup_file)
    else:
        parser.print_help()

if __name__ == '__main__':
    asyncio.run(main())
