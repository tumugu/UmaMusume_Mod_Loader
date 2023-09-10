import PySimpleGUI as sg

from PIL import Image
import sqlite3
import json

from os.path import join,isdir,exists,split
from os import getlogin,listdir

from pprint import pprint


pack_format = 1
user_name = getlogin()

# def mod_check():
#     with open(join(".",".umml","mod_check.json"),mode="r",encoding="utf-8") as f:
#         mod_check_json = json.load(f)

#     for mod_check in mod_check_json["mod"]:
#         for i in meta:
#             if mod_check_json in i:
#                 print(F"{i}あるよ")


def theme_set():
    with open(join(".",".umml","config.json"),mode="r",encoding="utf-8")as f:
        umamusume_theme = json.load(f)["config"]["theme"]

    sg.theme_add_new('UmaMusume', umamusume_theme)
    sg.theme("UmaMusume")

    return None


# def meta_get(mod_path):
#     assets_exists = isdir(join(mod_path,"assets")) # assetsがあったらTrueを返す
#     sql_exists = exists(join(mod_path,"sql","load")) and exists(join(mod_path,"sql","unload")) # sql/load と sql/unload があるとTrueを返す

#     with open(join(mod_path, "meta.json"), mode="r", encoding="utf-8") as f:
#         meta_json = json.load(f)

#     meta = {
#         split(mod_path)[1] : {
#             "pack_format" : meta_json["meta"]["pack_format"],
#             "name"        : meta_json["meta"]["name"],
#             "description" : meta_json["meta"]["description"],
#             "version"     : meta_json["meta"]["version"],
#             "assets"      : assets_exists,
#             "sql"         : sql_exists
#         }
#     }
    
#     return meta


# theme_set()

mods_layout = []


# for folder_name in listdir(join(".","mods")):
#     meta = meta_get(join(".","mods",folder_name))
#     print(meta)

# mod_check()
#     mods_layout.extend(
#         [
#             [
#                 sg.Frame("",[[sg.Image(filename=join(".","mods",folder_name,"mod_pack.png"),subsample=int(Image.open(join(".","mods",folder_name,"mod_pack.png")).size[0]/100),size=(100,100)),sg.Column([[sg.Text(meta["name"]),sg.Push(),sg.Button("詳細",key=folder_name,size=(5,1)),sg.Button("▶",size=(3,1))],[sg.Frame("",relief=sg.RELIEF_RIDGE,background_color="#FFFFFF",layout=[[sg.Text(meta["description"],background_color="#FFFFFF",size=(36,4))]])]])]])
#             ],
#         ]
#     )



mods_dict = {}

with open(join(".",".umml","info.json"), mode="r",encoding="utf-8") as f:
    info = json.load(f)


for folder_name in listdir(join(".","mods")):
    with open(join(".","mods", folder_name, "meta.json"), mode="r", encoding="utf-8") as f:
        meta_dict = json.load(f)
    
    if folder_name not in info["info"]:

        mod_info = {
            folder_name : {
                "isSelected" : False
            }
        }

        info["info"].update(mod_info)
    
    if info["info"][folder_name]["isSelected"] == True:
        meta_dict["meta"]["isSelected"] = True
    else:
        meta_dict["meta"]["isSelected"] = False

    mods_dict.update({folder_name: meta_dict["meta"]})


with open(join(".",".umml","info.json"),mode="w",encoding="utf-8") as f:
    json.dump(info,f,indent=4,ensure_ascii=False)


for mod in mods_dict:
    pass

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


main_layout = [
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


sub_layot = [
    [
        sg.Text()
    ]
]


def main():
    main_window = sg.Window("UmaMusume_Mod_Loader",main_layout,size=(1000,500),finalize=True)
    sub_window = sg.Window("詳細",sub_layot)

    while True:
        window, event, values = sg.read_all_windows()


        for mod_folder_name in listdir(join(".","mods")):
            if event == mod_folder_name:
                print(mod_folder_name)
                         
        if event == sg.WIN_CLOSED:
            if window == main_window:
                break
            if window == sub_window:
                sub_window.close()


if __name__ == "__main__":
    # main()
    pass