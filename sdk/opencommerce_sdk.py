import json
import os
from eth_account import Account
from pathlib import Path
import requests
from web3 import Web3
from dotenv import load_dotenv
import logging
import webbrowser
from eth_account.datastructures import SignedTransaction
from datetime import datetime

load_dotenv()

class ServiceDirectory:
    BASE_URL = "https://servicedirectory-production.up.railway.app"

    @staticmethod
    def get_service(service_id: str) -> dict:
        """Get service information from the public API"""
        try:
            response = requests.get(f"{ServiceDirectory.BASE_URL}/services/by-name/{service_id}")
            if response.status_code == 200:
                service_data = response.json()
                return {
                    'address': service_data['service_metadata']['address'],
                    'cost': service_data['service_metadata']['cost'],
                    'url': service_data['url']
                }
            else:
                raise ValueError(f"Service '{service_id}' not found")
        except Exception as e:
            logging.error(f"Error fetching service info: {str(e)}")
            raise

    @staticmethod
    def list_services() -> list:
        """List all available services"""
        try:
            response = requests.get(f"{ServiceDirectory.BASE_URL}/services/")
            if response.status_code == 200:
                return response.json()
            else:
                raise Exception("Failed to fetch services list")
        except Exception as e:
            logging.error(f"Error listing services: {str(e)}")
            raise

class OpenCommerceAccountToolkit:
    ADDRESS_TRACKER_URL = "https://address-tracker-service-production.up.railway.app"
    # Network-specific contract addresses
    NETWORK_CONFIG = {
        'testnet': {
            'usdc_address': '0x036CbD53842c5426634e7929541eC2318f3dCF7e',
            'rpc_url': 'https://base-sepolia.infura.io/v3/4f2c3c8c48da4d1eafa668260e7840bd',
            'network_name': 'base-sepolia'
        },
        'production': {
            'usdc_address': '0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913',
            'rpc_url': 'https://base-mainnet.infura.io/v3/4f2c3c8c48da4d1eafa668260e7840bd',
            'network_name': 'base'
        }
    }

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
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

    def __init__(
        self,
        account_file: str = 'account.json',
        passphrase: str = None,
        stablecoin_symbol: str = 'USDC',
        network: str = 'testnet'
    ):
        # Silence all third-party logging
        logging.getLogger('web3').setLevel(logging.WARNING)
        logging.getLogger('urllib3').setLevel(logging.WARNING)
        logging.getLogger('requests').setLevel(logging.WARNING)
        logging.getLogger('httpx').setLevel(logging.WARNING)
        logging.getLogger('urllib3.connectionpool').setLevel(logging.WARNING)
        logging.getLogger('asyncio').setLevel(logging.WARNING)
        logging.getLogger('ssl').setLevel(logging.WARNING)
        logging.getLogger('http.client').setLevel(logging.WARNING)

        # Also disable propagation of logs from these loggers
        for logger_name in ['web3', 'urllib3', 'requests', 'httpx', 'asyncio', 'ssl']:
            logger = logging.getLogger(logger_name)
            logger.propagate = False

        logging.info("Initializing OpenCommerce SDK...")
        self.account_file = account_file
        self.passphrase = passphrase or 'default_passphrase'
        self.stablecoin_symbol = stablecoin_symbol.upper()
        self.network = network.lower()
        
        if self.network not in self.NETWORK_CONFIG:
            raise ValueError(f"Invalid network: {network}. Must be one of: {list(self.NETWORK_CONFIG.keys())}")
        
        self.network_config = self.NETWORK_CONFIG[self.network]
        self.USDC_CONTRACT_ADDRESS = self.network_config['usdc_address']
        
        self.w3 = self.initialize_web3()
        self.user_account = self.initialize_account()
        self.register_address()
        logging.info(f"Account initialized on {self.network}: {self.get_account_address()[:8]}...")
        self.check_and_prompt_funding()

    def initialize_web3(self):
        rpc_url = self.network_config['rpc_url']
        if not rpc_url:
            logging.error(f"{self.network_config['rpc_url']} environment variable is not set")
            raise ValueError(f"{self.network_config['rpc_url']} environment variable is not set")
        logging.info(f"Connecting to {self.network} RPC URL: {rpc_url}")
        return Web3(Web3.HTTPProvider(rpc_url))

    def initialize_account(self):
        logging.info(f"Initializing account from file: {self.account_file}")
        try:
            if Path(self.account_file).is_file():
                with open(self.account_file, 'r') as f:
                    encrypted_key = json.load(f)
                    private_key = Account.decrypt(encrypted_key, self.passphrase)
                    account = Account.from_key(private_key)
                    logging.info("Account loaded from file.")
            else:
                raise FileNotFoundError
        except (FileNotFoundError, json.JSONDecodeError, ValueError) as e:
            logging.warning(f"Error loading account: {str(e)}. Creating new account...")
            account = Account.create()
            encrypted_key = Account.encrypt(account._private_key, self.passphrase)
            with open(self.account_file, 'w') as f:
                json.dump(encrypted_key, f)
            logging.info("New account created and saved to file.")
        return account
    
    def register_address(self):
        """Register the account address with the tracking service"""
        try:
            payload = {
                "address": self.get_account_address(),
                "network": self.network_config['network_name'],
                "metadata": {
                    "sdk_version": "1.1.0",
                    "initialization_time": datetime.utcnow().isoformat(),
                    "client_type": "opencommerce_sdk"
                }
            }
            
            response = requests.post(
                f"{self.ADDRESS_TRACKER_URL}/register_address",
                json=payload,
                headers={"Content-Type": "application/json"},
                timeout=10
            )
            
            if response.status_code == 200:
                logging.info(f"Address {self.get_account_address()[:8]}... registered successfully")
            else:
                logging.warning(f"Failed to register address: {response.status_code} - {response.text}")
                
        except Exception:
            # Silently fail - tracking is optional
            pass

    def get_account_address(self):
        return self.user_account.address

    def check_balance(self):
        eth_balance = self.w3.eth.get_balance(self.get_account_address())
        eth_balance_eth = self.w3.from_wei(eth_balance, 'ether')

        usdc_contract = self.w3.eth.contract(address=self.USDC_CONTRACT_ADDRESS, abi=self.USDC_ABI)
        usdc_balance = usdc_contract.functions.balanceOf(self.get_account_address()).call()
        usdc_balance_decimal = usdc_balance / 1e6

        if eth_balance > 0 or usdc_balance > 0:
            logging.info(f"Balance - ETH: {eth_balance_eth}, USDC: {usdc_balance_decimal}")

        return eth_balance, usdc_balance

    def check_and_prompt_funding(self):
        logging.info("Checking if funding is needed")
        eth_balance, usdc_balance = self.check_balance()
        if eth_balance == 0 or usdc_balance == 0:
            logging.warning("Insufficient balance detected. Showing funding widget.")
            self.show_funding_widget()

    def show_funding_widget(self):
        widget_url = "https://fundingwidget-production.up.railway.app/"
        full_url = f"{widget_url}?wallet={self.get_account_address()}"
        
        logging.info("Opening funding interface...")
        webbrowser.open(full_url)
        input("Press Enter when you've completed the funding process...")
        self.check_balance()

    def use_service(self, service_id: str, params: dict) -> dict:
        logging.info(f"Initiating service call to {service_id}")
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

            nonce = self.w3.eth.get_transaction_count(self.get_account_address())
            
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

            signed_txn = self.user_account.sign_transaction(txn)

            if not isinstance(signed_txn, SignedTransaction):
                raise TypeError(f"Expected SignedTransaction, got {type(signed_txn)}")
            
            if not hasattr(signed_txn, 'raw_transaction'):
                raise AttributeError("SignedTransaction missing 'raw_transaction' attribute")

            raw_tx_bytes = signed_txn.raw_transaction
            raw_tx_hex = raw_tx_bytes.hex()

            backend_url = "https://web-production-5c8af.up.railway.app"  # Update with actual backend URL
            payload = {
                "signed_tx": raw_tx_hex,
                "service_id": service_id,
                "params": params
            }
            logging.info(f"Sending payload to backend: {payload}")
            logging.debug(f"Payload details: signed_tx length: {len(payload['signed_tx'])}, service_id: {payload['service_id']}, params: {payload['params']}")
            
            response = requests.post(
                f"{backend_url}/send_transaction",
                json=payload,
                headers={"Content-Type": "application/json"}
            )

            logging.info(f"Backend response status: {response.status_code}")
            logging.debug(f"Backend response: {response.text}")

            if response.status_code == 200:
                result = response.json()
                logging.info(f"Service {service_id} call completed successfully")
                return result["service_response"]
            else:
                raise Exception(f"Backend request failed: {response.text}")

        except Exception as e:
            logging.error(f"Service call failed: {str(e)}")
            raise

    def test_connection(self):
        logging.info("Testing connection to Base Sepolia")
        try:
            block = self.w3.eth.get_block('latest')
            logging.info(f"Successfully connected to Base Sepolia. Latest block number: {block.number}")
        except Exception as e:
            logging.error(f"Failed to connect to Base Sepolia: {str(e)}")

    def send_transaction(self, signed_txn):
        logging.info("Sending raw transaction")
        tx_hash = self.w3.eth.send_raw_transaction(signed_txn.rawTransaction)
        logging.info(f"Transaction sent. Hash: {tx_hash.hex()}")
        return tx_hash
