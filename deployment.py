import json
from web3 import Web3
from solcx import compile_standard, install_solc
import connect
import edit


# compile the contract
print("compiling contract...")
with open("./TESLA.sol", "r") as file:
    options_file = file.read()

install_solc("0.8.9")
compiled_sol = compile_standard(
    {
        "language": "Solidity",
        "sources": {"TESLA.sol": {"content": options_file}},
        "settings": {
            "outputSelection": {
                "*": {
                    "*": [
                        "abi",
                        "metadata",
                        "evm.bytecode",
                        "evm.bytecode.sourceMap",
                    ]
                }
            }
        },
    },
    solc_version="0.8.9",
)

with open("./compiled_tesla.json", "w") as file:
    json.dump(compiled_sol, file)

print("contract successfully compiled!")


# get contract abi and bytecode
print("computing contract abi and bytecode...")
with open("./compiled_tesla.json", "r") as file:
    source_json = json.load(file)

bytecode_ = source_json["contracts"]["TESLA.sol"]["TESLA"]["evm"]["bytecode"]["object"]

abi_ = source_json["contracts"]["TESLA.sol"]["TESLA"]["abi"]


w3, chain_id = connect.to_chain()

my_address = input("Input public key:")
private_key_ = input("Input private key (Hexdecimal form):")
nonce = w3.eth.getTransactionCount(my_address)

# use abi and bytecode to create the contract and get it ready for deployment
Options = w3.eth.contract(abi=abi_, bytecode=bytecode_)
transaction = Options.constructor().buildTransaction(
    {"chainId": chain_id, "nonce": nonce, "from": my_address}
)

print("deploying smart contract...")
# sign the txn and deploy contraact
signed_txn = w3.eth.account.sign_transaction(transaction, private_key=private_key_)
tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)

# wait or transaction to take place
tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
print(f"Success! Contract deployed to {tx_receipt.contractAddress}")

# reset the datasets so that they are ready to be used by other programs
contract_address = str(tx_receipt.contractAddress)
edit.reset(contract_address)
