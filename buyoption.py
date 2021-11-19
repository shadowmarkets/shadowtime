from web3 import Web3
import json
import pandas as pd
import connect


def buy(counter, public_key, private_key):

    w3, chain_id = connect.to_chain()
    options_contract = connect.to_contract(w3)

    nonce = w3.eth.getTransactionCount(public_key)

    price = options_contract.functions.get_price(counter).call()

    buy_option_txn = options_contract.functions.buyoption(counter).buildTransaction(
        {
            "chainId": chain_id,
            "from": public_key,
            "nonce": nonce,
            "value": price,
        }
    )

    connect.make_txn(w3, buy_option_txn, private_key)
    print("successfully bought option!!")