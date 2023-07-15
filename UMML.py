import PySimpleGUI as sg
import sqlite3
import json
import os

user_name = os.getlogin()

def mod_get(_mod_path):
    with open(os.path.join(_mod_path,"meta.json"),mode="r",encoding="utf-8")as f:
        _meta_json = json.load(f)
    _mod_meta = {
        "pack_format":_meta_json["meta"]["pack_format"],
        "mod_name":_meta_json["meta"]["mod_name"],
        "description":_meta_json["meta"]["description"],
        "version":_meta_json["meta"]["version"],
        "assets":os.path.isdir(os.path.join(_mod_path,"assets")),
        "sql":os.path.isdir(os.path.join(_mod_path,"sql"))
    }
    
    return _mod_meta


umamusume_theme = {
    'BACKGROUND': '#fafbfa',
    'TEXT': '#794016',
    'INPUT': '#FFFFFF',
    'TEXT_INPUT': '#794016',
    'SCROLL': '#c7e78b',
    'BUTTON': ('#ffffff', '#7DCC0A'),
    'PROGRESS': ('#7DCC0A', '#DCDCDC'),
    'BORDER': 1,
    'SLIDER_DEPTH': 0,
    'PROGRESS_DEPTH': 0,
}

mods_list = os.listdir("./mods")

for i in mods_list:
    a = mod_get(os.path.join("./mods",i))
    print(a)



sg.theme_add_new('UmaMusume', umamusume_theme)
sg.theme("UmaMusume")

top_layout = [
    [
        sg.Push(),
        sg.Text("ウマ娘モッドの選択"),
        sg.Push()
    ],
    [
        sg.Push(),
        sg.Text("ウマ娘のモッドをガチャガチャすると入れられます"),
        sg.Push()
    ]
]

center_layout = [
    [
        sg.Frame("",[[
            sg.Column([
                [
                    sg.Frame("",[[sg.Image(filename=RF"C:\Users\{user_name}\Documents\python\temp\lb-tank02.png",size=(70,70)),sg.Column([[sg.Text("タイトル",font=("Arial Black",10)),sg.Push(),sg.Button("→",size=(3,1))],[sg.Multiline("",size=(45,2))]])]])
                ]
            ],scrollable=True,vertical_scroll_only=True,size=(450,350))
        ]]),

        sg.Push(),

        sg.Frame("",[[
            sg.Column([
                [
                    sg.Frame("mod名",[[sg.Image(filename=RF"C:\Users\{user_name}\Documents\python\temp\lb-tank02.png",expand_x=True,expand_y=True),sg.Column([[sg.Text("タイトル",font=("Arial Black",10)),sg.Push(),sg.Button("→")],[sg.Multiline("",size=(43,2))]])]])
                ]
            ],scrollable=True,vertical_scroll_only=True,size=(450,350))
        ]]),
    ]
]

under_layout = [
    [
        sg.Frame("",[
            [
                sg.Text("aaa")
            ]
        ])
    ]
]

layout = [
    [
        sg.Column(top_layout,justification="c"),
    ],
    [
        sg.Column(center_layout)
    ],
    [
        sg.Column(under_layout)
    ]
]

window = sg.Window("UmaMusume_Mod_Loader",layout,size=(1000,500))

while True:
    event,values = window.read()

    if event == sg.WIN_CLOSED:
        break

window.close()