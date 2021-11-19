import pandas as pd
from web3 import Web3
import json
import connect


def create(
    leverage, cap, strike, price, expiry_str, expiry_int, public_key, private_key
):
    w3, chain_id = connect.to_chain()
    options_contract = connect.to_contract(w3)
    nonce = w3.eth.getTransactionCount(public_key)

    deposit = int(leverage) * int(cap)
    create_option_txn = options_contract.functions.createoption(
        leverage, cap, int(strike * 100), price, expiry_str, expiry_int
    ).buildTransaction(
        {
            "chainId": chain_id,
            "from": public_key,
            "nonce": nonce,
            "value": deposit * (10 ** 18),
        }
    )

    connect.make_txn(w3, create_option_txn, private_key)
    print("successfully created option!!")
