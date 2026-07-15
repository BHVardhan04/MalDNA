import os
import json
import hashlib
import logging
from datetime import datetime
from typing import Dict, Any, Optional, Union
from web3 import Web3

# ✅ Logging Configuration
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

# ✅ Load Blockchain Environment
BLOCKCHAIN_RPC_URL = os.getenv("BLOCKCHAIN_RPC_URL", "http://localhost:8545")
SMART_CONTRACT_ADDRESS = os.getenv("SMART_CONTRACT_ADDRESS")
PRIVATE_KEY = os.getenv("BLOCKCHAIN_PRIVATE_KEY")
CONTRACT_ABI_PATH = os.getenv("CONTRACT_ABI_PATH")

# ✅ Connect to Blockchain
web3 = None
contract = None
account = None

try:
    if not SMART_CONTRACT_ADDRESS or not PRIVATE_KEY or not CONTRACT_ABI_PATH:
        raise ValueError("Missing blockchain configuration environment variables")

    web3 = Web3(Web3.HTTPProvider(BLOCKCHAIN_RPC_URL))
    if not web3.is_connected():
        raise ConnectionError("❌ Failed to connect to the blockchain network")

    # ✅ Load ABI and Contract
    with open(CONTRACT_ABI_PATH, "r") as f:
        contract_data = json.load(f)

    contract = web3.eth.contract(
        address=Web3.to_checksum_address(SMART_CONTRACT_ADDRESS),
        abi=contract_data["abi"] if isinstance(contract_data, dict) else contract_data
    )
    account = web3.eth.account.from_key(PRIVATE_KEY)
except Exception as e:
    logger.warning(f"⚠️ Blockchain configuration or connection failed: {e}. Blockchain features will be disabled.")

# 🧬 Generate DNA Hash
def generate_dna(data: Any) -> bytes:
    """Generates a DNA hash from the provided data"""
    json_data = json.dumps(data, sort_keys=True).encode()
    return Web3.keccak(json_data)

# 🧬 Store Malware on Blockchain (No Stake)
def store_on_blockchain(data: Any, metadata: Optional[Dict[str, Any]] = None) -> Dict[str, str]:
    """Store malware on the blockchain if not already present"""
    try:
        dna_hash = generate_dna(data)

        try:
            existing = contract.functions.getMalware(dna_hash).call()
            if existing[0] != b'\x00' * 32 and any(existing):
                logger.info("⚠️ Malware already stored on blockchain")
                return {"status": "already_exists", "dna_hash": dna_hash.hex()}
        except Exception as check_error:
            logger.warning(f"⚠️ Could not verify existing malware: {check_error}")

        nonce = web3.eth.get_transaction_count(account.address)
        tx = contract.functions.submitMalware(dna_hash).build_transaction({
            "from": account.address,
            "nonce": nonce,
            "gas": 300000,
            "gasPrice": web3.to_wei(20, "gwei")
        })

        signed_txn = web3.eth.account.sign_transaction(tx, PRIVATE_KEY)
        tx_hash = web3.eth.send_raw_transaction(signed_txn['rawTransaction'])

        logger.info(f"✅ Malware submitted. TX ID: {tx_hash.hex()}")
        return {"dna_hash": dna_hash.hex(), "tx_id": tx_hash.hex(), "status": "success"}

    except Exception as e:
        logger.error(f"❌ Blockchain storage failed: {e}")
        return {"error": str(e), "status": "failed"}

# ✅ Verify Malware on Blockchain (only malware_dna required)
def verify_on_blockchain(data: Any) -> bool:
    """Verify if the malware exists on the blockchain"""
    try:
        dna_hash = generate_dna(data)
        malware = contract.functions.getMalware(dna_hash).call()
        is_verified = malware[0].hex() == dna_hash.hex()

        logger.info(f"{'✅ Verified' if is_verified else '⚠️ Not Verified'} for DNA: {dna_hash.hex()}")
        return is_verified

    except Exception as e:
        logger.error(f"❌ Verification failed for DNA: {e}")
        return False

# 🤖 AI Classification with Forensic Metadata
def classify_malware(data: Any, classification: str, model_version: str = "v1") -> Dict[str, str]:
    """Classify malware with forensic metadata"""
    try:
        dna_hash = generate_dna(data)
        nonce = web3.eth.get_transaction_count(account.address)

        tx = contract.functions.classifyMalware(dna_hash, classification).build_transaction({
            "from": account.address,
            "nonce": nonce,
            "gas": 250000,
            "gasPrice": web3.to_wei(20, "gwei")
        })

        signed_txn = web3.eth.account.sign_transaction(tx, PRIVATE_KEY)
        tx_hash = web3.eth.send_raw_transaction(signed_txn['rawTransaction'])

        logger.info(f"✅ Classified {dna_hash.hex()} as {classification} (Model: {model_version}). TX: {tx_hash.hex()}")
        return {"tx_id": tx_hash.hex(), "status": "success"}

    except Exception as e:
        logger.error(f"❌ Classification failed: {e}")
        return {"error": str(e), "status": "failed"}

# 📊 Reputation Query (based on malware DNA or Ethereum address)
def get_reputation(identifier: Union[str, bytes]) -> Dict[str, Any]:
    """Query reputation for a given address or malware DNA"""
    try:
        if isinstance(identifier, str):
            if identifier.startswith("0x") and len(identifier) == 42:
                address = Web3.to_checksum_address(identifier)
            else:
                address = Web3.to_checksum_address(account.address)  # default
        elif isinstance(identifier, bytes):
            address = Web3.to_checksum_address(account.address)  # default
        else:
            raise ValueError("Invalid identifier")

        rep = contract.functions.getReputation(address).call()
        return {
            "points": rep[0],
            "last_updated": datetime.utcfromtimestamp(rep[1]).isoformat()
        }
    except Exception as e:
        logger.error(f"❌ Get reputation failed: {e}")
        return {"error": str(e)}
# 🗳️ Public Malware Voting (No Role Check)
def vote_on_malware(data: Any, approve: bool) -> Dict[str, str]:
    """Allow public users to vote on the malware approval (no admin/role checks)"""
    try:
        dna_hash = generate_dna(data)
        nonce = web3.eth.get_transaction_count(account.address)

        tx = contract.functions.voteOnMalware(dna_hash, approve).build_transaction({
            "from": account.address,
            "nonce": nonce,
            "gas": 250000,
            "gasPrice": web3.to_wei(20, "gwei")
        })

        signed_txn = web3.eth.account.sign_transaction(tx, PRIVATE_KEY)
        tx_hash = web3.eth.send_raw_transaction(signed_txn['rawTransaction'])

        logger.info(f"✅ Vote {'approved' if approve else 'rejected'} for {dna_hash.hex()}. TX: {tx_hash.hex()}")
        return {"tx_id": tx_hash.hex(), "status": "success"}

    except Exception as e:
        logger.error(f"❌ Vote failed: {e}")
        return {"error": str(e), "status": "failed"}

# 🔍 Blockchain Forensic Metadata
def extract_blockchain_metadata(tx_hash: str) -> Optional[Dict[str, Any]]:
    """Extract forensic metadata from a blockchain transaction"""
    try:
        tx_receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
        block_number = tx_receipt.blockNumber
        gas_used = tx_receipt.gasUsed
        block = web3.eth.get_block(block_number)
        timestamp = block.timestamp
        tx = web3.eth.get_transaction(tx_hash)

        metadata = {
            "tx_hash": tx_hash,
            "gas_used": gas_used,
            "gas_price": tx.gasPrice,
            "block_number": block_number,
            "from": tx["from"],
            "to": tx["to"],
            "timestamp": datetime.utcfromtimestamp(timestamp).isoformat(),
            "chain_id": tx.chainId,
            "cross_chain": {
                "source": BLOCKCHAIN_RPC_URL,
                "destination": "tbd",
                "status": "pending"
            }
        }
        logger.info(f"📦 Metadata Extracted: {metadata}")
        return metadata

    except Exception as e:
        logger.error(f"❌ Metadata extraction failed: {e}")
        return None

