import pandas as pd
import json
from web3 import Web3
import requests
import connect

import sys


latest_close_date = input(
    "which options do you want to resolve, e.g. on what day did they expire (in format yyyy-mm-dd)?"
)

url = "https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol=TSLA&apikey=0F1FJH5TJ28W5ZZH"
r = requests.get(url)
alpha_vantage_data = r.json()
latest_close = alpha_vantage_data["Time Series (Daily)"][latest_close_date]["4. close"]
closing_value = int(float(latest_close) * 100)


w3, chain_id = connect.to_chain()
options_contract = connect.to_contract(w3)


my_address = input("Input public key:")
private_key = input("Input private key (Hexdecimal form):")
nonce = w3.eth.getTransactionCount(my_address)


print("calling resolution function...")

create_option_txn = options_contract.functions.resolution(
    closing_value, latest_close_date
).buildTransaction(
    {
        "chainId": chain_id,
        "from": my_address,
        "nonce": nonce,
    }
)

signed_create_option_txn = w3.eth.account.sign_transaction(
    create_option_txn,
    private_key=private_key,
)
tx_create_option_hash = w3.eth.send_raw_transaction(
    signed_create_option_txn.rawTransaction
)

tx_receipt = w3.eth.wait_for_transaction_receipt(tx_create_option_hash)
print("successfully resolved options that expired on ", latest_close_date)
