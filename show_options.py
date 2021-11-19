import PySimpleGUI as sg
import pandas as pd
from pandas.core.frame import DataFrame
import connect


def show():
    w3, chain_id = connect.to_chain()
    options_contract = connect.to_contract(w3)

    number = options_contract.functions.get_length().call()
    df = pd.DataFrame(
        columns=[
            "Number",
            "Leverage",
            "Cap",
            "Strike (in USD)",
            "Price (in ETH)",
            "Expiry date",
            "Expiry blockstamp",
        ]
    )

    for x in range(0, number):
        if options_contract.functions.get_available(x).call() == True:
            leverage = options_contract.functions.get_leverage(x).call()
            cap = options_contract.functions.get_cap(x).call()
            strike = options_contract.functions.get_strike(x).call() / 100
            price = options_contract.functions.get_price(x).call() / (10 ** 18)
            date = options_contract.functions.get_expirystr(x).call()
            blocktime = options_contract.functions.get_expiryint(x).call()
            df = df.append(
                DataFrame(
                    {
                        "Number": x,
                        "Leverage": leverage,
                        "Cap": cap,
                        "Strike (in USD)": strike,
                        "Price (in ETH)": price,
                        "Expiry date": date,
                        "Expiry blockstamp": blocktime,
                    },
                    index=[x],
                )
            )
    else:
        pass

    data = df.values.tolist()
    header_list = list(df.columns)
    data = df[0:].values.tolist()

    layout = [
        [sg.Text("These are the available options")],
        [
            sg.Table(
                values=data,
                headings=header_list,
                display_row_numbers=False,
                auto_size_columns=False,
                num_rows=min(1000, len(data)),
            )
        ],
        [sg.Text("Current block timesptamp is:")],
        [sg.Text(options_contract.functions.get_time().call())],
    ]

    window = sg.Window("Table", layout, grab_anywhere=False)
    event, values = window.read()
    window.close()
