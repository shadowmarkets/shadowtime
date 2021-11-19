import PySimpleGUI as sg
import buyoption
import show_options


def buy(public_key, private_key):

    layout = [
        [sg.Text("Press VIEW to see available options")],
        [sg.Button("VIEW")],
        [sg.Text("Which option would you like to buy (enter N)")],
        [sg.Input(key="NUMBER")],
        [sg.Button("BUY", bind_return_key=True), sg.Button("CANCEL")],
    ]

    window = sg.Window("Buy Options", layout)

    while True:
        event, values = window.read()
        print(event, values)
        if event == "VIEW":
            show_options.show()
        elif event == "BUY":
            buyoption.buy(int(values["NUMBER"]), public_key, private_key)
        else:
            break

    window.close()
