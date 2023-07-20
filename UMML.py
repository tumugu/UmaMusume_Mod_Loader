import PySimpleGUI as sg

from PIL import Image
import sqlite3
import json

from os.path import join,isdir,exists
from os import getlogin,listdir

from pprint import pprint


pack_format = 1
user_name = getlogin()

def theme_set():
    with open(join(".","config","config.json"),mode="r",encoding="utf-8")as f:
        umamusume_theme = json.load(f)["config"]["theme"]

    sg.theme_add_new('UmaMusume', umamusume_theme)
    sg.theme("UmaMusume")

    return None

def meta_get(mod_path):
    assets_exists = isdir(join(mod_path,"assets")) # assetsがあったらTrueを返す
    sql_exists = exists(join(mod_path,"sql","load")) and exists(join(mod_path,"sql","unload")) # sql/load と sql/unload があるとTrueを返す

    with open(join(mod_path, "meta.json"), mode="r", encoding="utf-8") as f:
        meta_json = json.load(f)

    meta = {
        "pack_format" : meta_json["meta"]["pack_format"],
        "name"        : meta_json["meta"]["name"],
        "description" : meta_json["meta"]["description"],
        "version"     : meta_json["meta"]["version"],
        "assets"      : assets_exists,
        "sql"         : sql_exists
    }
    
    return meta


theme_set()

mods_layout = []

for i in listdir(join(".","mods")):
    a = meta_get(join(".","mods",i))
    mods_layout.extend(
        [
            [
                sg.Frame("",[[sg.Image(filename=join(".","mods",i,"mod_pack.png"),subsample=int(Image.open(join(".","mods",i,"mod_pack.png")).size[0]/100),size=(100,100)),sg.Column([[sg.Text(a["name"]),sg.Push(),sg.Button("詳細",size=(5,1)),sg.Button("▶",size=(3,1))],[sg.Frame("",relief=sg.RELIEF_RIDGE,background_color="#FFFFFF",layout=[[sg.Text(a["description"],background_color="#FFFFFF",size=(36,4))]])]])]])
            ],
        ]
    )



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
            sg.Column(mods_layout,scrollable=True,vertical_scroll_only=True,size=(450,400))
        ]]),

        sg.Push(),

        sg.Frame("",[[
            sg.Column(
                [[]],scrollable=True,vertical_scroll_only=True,size=(450,400))
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



def main():
    window = sg.Window("UmaMusume_Mod_Loader",layout,size=(1000,500))

    while True:
        event,values = window.read()

        if event == sg.WIN_CLOSED:
            break

    window.close()



if __name__ == "__main__":
    main()
