import pandas as pd

# resets the datasets
def reset(address):

    address_str = str(address)
    data = pd.read_csv("./info.csv")

    data._set_value(int(0), "TSLA", "0")
    data._set_value(int(1), "TSLA", address_str)
    data.to_csv("./info.csv", index=False)
