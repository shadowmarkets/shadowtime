import PySimpleGUI as sg
import createoption


def create(public_key, private_key):
    layout = [
        [sg.Text("LEVERAGE")],
        [sg.Input(key="leverage")],
        [sg.Text("CAP")],
        [sg.Input(key="cap")],
        [sg.Text("STRIKE")],
        [sg.Input(key="strike")],
        [sg.Text("PRICE")],
        [sg.Input(key="price")],
        [sg.Text("What day should this option expire (in form yyyy-mm-dd)")],
        [sg.Input(key="exp_str")],
        [sg.Text("In how long does it expire")],
        [sg.Text("In this Beta input a value in how many minutes!")],
        [sg.Input(key="exp_int")],
        [sg.Button("CREATE", bind_return_key=True), sg.Button("CANCEL")],
    ]

    window = sg.Window("Create Options", layout)

    while True:
        event, values = window.read()
        print(event, values)
        if event == "CREATE":
            createoption.create(
                int(values["leverage"]),
                int(values["cap"]),
                float(values["strike"]),
                int(values["price"]),
                str(values["exp_str"]),
                int(values["exp_int"]),
                public_key,
                private_key,
            )
        else:
            break

    window.close()
