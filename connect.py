from web3 import Web3
import json
import pandas as pd


def to_chain():
    print("connecting to blockchain...")
    w3 = Web3(Web3.HTTPProvider("HTTP://127.0.0.1:7545"))
    chain_id = 1337
    return w3, chain_id


def to_contract(w3):

    print("connecting to smart contract...")
    k = pd.read_csv("./info.csv")

    with open("./compiled_tesla.json", "r") as file:
        source_json = json.load(file)

    abi_ = source_json["contracts"]["TESLA.sol"]["TESLA"]["abi"]
    contract_address = k.loc[1]["TSLA"]

    return w3.eth.contract(address=contract_address, abi=abi_)


def make_txn(w3, txn, private_key):
    signed_create_option_txn = w3.eth.account.sign_transaction(
        txn,
        private_key=private_key,
    )
    tx_create_option_hash = w3.eth.send_raw_transaction(
        signed_create_option_txn.rawTransaction
    )

    tx_receipt = w3.eth.wait_for_transaction_receipt(tx_create_option_hash)
