import PySimpleGUI as sg
import create_gui
import buy_gui


layout = [
    [sg.Text("Enter account (public key)")],
    [sg.Input(key="public_key")],
    [sg.Text("Enter private key in hexdecimal form")],
    [sg.Input(key="private_key")],
    [sg.Text("Do you want to create or buy an option?")],
    [sg.Button("CREATE"), sg.Button("BUY"), sg.Button("CANCEL")],
]

window = sg.Window("SHADOWMARKETS", layout)

while True:
    event, values = window.read()
    print(event, values)
    if event == "CREATE":
        create_gui.create(values["public_key"], values["private_key"])

    elif event == "BUY":
        buy_gui.buy(values["public_key"], values["private_key"])

    else:
        break

window.close()
