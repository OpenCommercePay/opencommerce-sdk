# opencommerce_sdk.py

import json
import os
import webbrowser
import logging
from pathlib import Path

from dotenv import load_dotenv
from eth_account import Account
from eth_account.datastructures import SignedTransaction
from web3 import Web3
import requests

try:
    from .service_directory import ServiceDirectory
except ImportError:
    from service_directory import ServiceDirectory

load_dotenv()

class OpenCommerceAccountToolkit:
    USDC_CONTRACT_ADDRESS = '0x036CbD53842c5426634e7929541eC2318f3dCF7e'
    USDC_ABI = [
        {
            "constant": False,
            "inputs": [
                {"name": "_to", "type": "address"},
                {"name": "_value", "type": "uint256"}
            ],
            "name": "transfer",
            "outputs": [{"name": "", "type": "bool"}],
            "type": "function"
        },
        {
            "constant": True,
            "inputs": [{"name": "_owner", "type": "address"}],
            "name": "balanceOf",
            "outputs": [{"name": "balance", "type": "uint256"}],
            "type": "function"
        }
    ]

    # Configure basic logging
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    def __init__(
        self,
        wallet_file: str = 'wallet.json',
        passphrase: str = None,
        stablecoin_symbol: str = 'USDC'
    ):
        logging.info("Initializing OpenCommerceAccountToolkit")
        self.wallet_file = wallet_file
        self.passphrase = passphrase or 'default_passphrase'
        self.stablecoin_symbol = stablecoin_symbol.upper()
        self.w3 = self.initialize_web3()
        self.user_account = self.initialize_wallet()
        logging.info(f"Wallet address: {self.get_wallet_address()}")
        self.check_and_prompt_funding()

    def initialize_web3(self):
        rpc_url = os.getenv('BASE_SEPOLIA_RPC_URL')
        if not rpc_url:
            logging.error("BASE_SEPOLIA_RPC_URL environment variable is not set")
            raise ValueError("BASE_SEPOLIA_RPC_URL environment variable is not set")
        logging.info(f"Connecting to Base Sepolia RPC URL: {rpc_url}")
        return Web3(Web3.HTTPProvider(rpc_url))

    def initialize_wallet(self):
        logging.info(f"Initializing wallet from file: {self.wallet_file}")
        try:
            if Path(self.wallet_file).is_file():
                with open(self.wallet_file, 'r') as f:
                    encrypted_key = json.load(f)
                    private_key = Account.decrypt(encrypted_key, self.passphrase)
                    account = Account.from_key(private_key)
                    logging.info("Wallet loaded from file.")
            else:
                raise FileNotFoundError
        except (FileNotFoundError, json.JSONDecodeError, ValueError) as e:
            logging.warning(f"Error loading wallet: {str(e)}. Creating new wallet...")
            account = Account.create()
            encrypted_key = Account.encrypt(account._private_key, self.passphrase)
            with open(self.wallet_file, 'w') as f:
                json.dump(encrypted_key, f)
            logging.info("New wallet created and saved to file.")
        return account

    def get_wallet_address(self):
        return self.user_account.address

    def check_balance(self):
        logging.info("Checking wallet balance")
        eth_balance = self.w3.eth.get_balance(self.get_wallet_address())
        eth_balance_eth = self.w3.from_wei(eth_balance, 'ether')
        logging.info(f"ETH balance: {eth_balance_eth} ETH")

        usdc_contract = self.w3.eth.contract(address=self.USDC_CONTRACT_ADDRESS, abi=self.USDC_ABI)
        usdc_balance = usdc_contract.functions.balanceOf(self.get_wallet_address()).call()
        usdc_balance_decimal = usdc_balance / 1e6  # USDC has 6 decimal places
        logging.info(f"USDC balance: {usdc_balance_decimal} USDC")

        return eth_balance, usdc_balance

    def check_and_prompt_funding(self):
        logging.info("Checking if funding is needed")
        eth_balance, usdc_balance = self.check_balance()
        if eth_balance == 0 or usdc_balance == 0:
            logging.warning("Insufficient balance detected. Showing funding widget.")
            self.show_funding_widget()

 # Need to change to actual funding widget URL 
    def show_funding_widget(self):
        widget_url = "http://localhost:3000"
        full_url = f"{widget_url}?wallet={self.get_wallet_address()}"

        logging.info(f"Opening funding widget: {full_url}")
        webbrowser.open(full_url)

        logging.info("Waiting for user to complete funding process...")
        input("Press Enter when you've completed the funding process...")

        logging.info("Re-checking balance after funding")
        self.check_balance()

    def use_service(self, service_id: str, params: dict) -> dict:
        logging.info(f"Attempting to use service: {service_id}")
        try:
            service_info = ServiceDirectory.get_service(service_id)
            if not service_info:
                logging.error(f"Service '{service_id}' not found")
                raise ValueError(f"Service '{service_id}' not found")

            eth_balance, usdc_balance = self.check_balance()
            if eth_balance == 0 or usdc_balance == 0:
                logging.warning("Insufficient balance. Showing funding widget.")
                self.show_funding_widget()
                return

            usdc_contract = self.w3.eth.contract(address=self.USDC_CONTRACT_ADDRESS, abi=self.USDC_ABI)

            amount = int(service_info['cost'] * 1e6)  # USDC has 6 decimal places
            logging.info(f"Service cost: {amount / 1e6} USDC")

            nonce = self.w3.eth.get_transaction_count(self.get_wallet_address())

            # Get the latest gas price
            gas_price = self.w3.eth.gas_price
            # Set maxPriorityFeePerGas to be 10% of the current gas price
            max_priority_fee = int(gas_price * 0.1)
            # Set maxFeePerGas to be the current gas price plus the maxPriorityFeePerGas
            max_fee = gas_price + max_priority_fee

            txn = usdc_contract.functions.transfer(
                service_info['address'],
                amount
            ).build_transaction({
                'chainId': self.w3.eth.chain_id,
                'gas': 200000,  # Adjust as needed
                'maxFeePerGas': max_fee,
                'maxPriorityFeePerGas': max_priority_fee,
                'nonce': nonce,
            })

            logging.debug(f"Transaction before signing: {txn}")
            signed_txn = self.user_account.sign_transaction(txn)
            logging.debug(f"Signed transaction: {signed_txn}")

            if not isinstance(signed_txn, SignedTransaction):
                logging.error(f"Expected SignedTransaction, got {type(signed_txn)}")
                raise TypeError(f"Expected SignedTransaction, got {type(signed_txn)}")

            raw_tx_hex = signed_txn.rawTransaction.hex()


            backend_url = "http://localhost:8000/send_transaction"  # Update with actual backend URL
            payload = {
                "signed_tx": raw_tx_hex,
                "service_id": service_id,
                "params": params
            }
            logging.info(f"Sending payload to backend: {payload}")

            response = requests.post(backend_url, json=payload, headers={"Content-Type": "application/json"})

            logging.info(f"Backend response status: {response.status_code}")
            logging.debug(f"Backend response: {response.text}")

            if response.status_code == 200:
                result = response.json()
                logging.info(f"Service {service_id} successfully called")
                return result["service_response"]
            else:
                logging.error(f"Backend request failed: {response.text}")
                raise Exception(f"Backend request failed: {response.text}")

        except Exception as e:
            logging.error(f"Error using service {service_id}: {str(e)}")
            raise

    def test_connection(self):
        logging.info("Testing connection to Base Sepolia")
        try:
            block = self.w3.eth.get_block('latest')
            logging.info(f"Successfully connected to Base Sepolia. Latest block number: {block.number}")
    
