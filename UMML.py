import PySimpleGUI as sg
import threading

sg.theme("default1")

layout = [
    [
        sg.Text("aaa")
    ]
]

window = sg.Window("UmaMusume_Mod_Loader",layout,size=(500,300))

# while True:
event,values = window.read()

#     if event == sg.WIN_CLOSED:
#         break

# window.close()