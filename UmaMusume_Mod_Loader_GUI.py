import os
import PySimpleGUI as sg
import yaml
import shutil
import sqlite3
import sys

sg.theme("Dark Brown")
modloader_version = "1.1.0"
need_key = ["mod_version","title","description","modloader_version"]

if os.path.isfile(".\\setting.yml"):
    with open(".\\setting.yml",encoding="utf-8") as yml:
        yaml_data = yaml.safe_load(yml)

    if yaml_data["umamusume_path"] == "default":
        dat_path = os.path.join("C:\\Users\\",os.getlogin(),"AppData\\LocalLow\\Cygames\\umamusume\\dat\\")
        master_path = os.path.join("C:\\Users\\",os.getlogin(),"AppData\\LocalLow\\Cygames\\umamusume\\master\\master.mdb")
    else:
        if os.path.isdir(yaml_data["umamusume_path"]):
            dat_path = os.path.join(yaml_data["umamusume_path"],"dat")
            master_path = os.path.join(yaml_data["umamusume_path"],"master","master.mdb")
        else:
            sg.popup_error("setting.ymlのumamusume_pathに書かれているフォルダが存在しません。\nパスを間違えている可能性があります。\nどうしても治らない場合はDMにてご報告よろしくお願いします。\nプログラムを終了します。")
            sys.exit()
else:
    sg.popup_error("setting.ymlが存在しません。パスをデフォルトにして起動します。")
    dat_path = os.path.join("C:\\Users\\",os.getlogin(),"AppData\\LocalLow\\Cygames\\umamusume\\dat\\")
    master_path = os.path.join("C:\\Users\\",os.getlogin(),"AppData\\LocalLow\\Cygames\\umamusume\\master\\master.mdb")

mod_load_layout = [
    [sg.Text("mod"),
    sg.InputText(key="-folder_path-",size=(43),enable_events=True),sg.FolderBrowse("参照"),
    sg.Button("更新",key="-reload-")
    ]
]

mod_info = [
    [sg.Text("",key="-title-")],
    [sg.Text("",key="-mod_version-")],
    [
    sg.Multiline(disabled=True,size=(60,10),key="-description-"),
    ]
]

mod_control = [
    [sg.Button("assetsロード",key="-assets_load-",disabled=True),
    sg.Button("assetsアンロード",key="-assets_unload-",disabled=True),
    ],
    [sg.Button("masterロード",key="-master_load-",disabled=True),
    sg.Button("masterアンロード",key="-master_unload-",disabled=True),
    sg.Text("modloader_version : 1.1.0",pad=((0,75),(0,0)))
    ]
]

progress = [
    [sg.Text("待機",key="-progress_value-")],
    [sg.ProgressBar(max_value=0, orientation="h", size=(36,20), key="-progress_bar-",bar_color=("SteelBlue1",""))],#E7C855
]

layout = [
    [sg.Frame("mod読み込み",mod_load_layout)],
    [sg.Frame("情報",mod_info)],
    [sg.Frame("管理",mod_control)],
    [sg.Frame("進捗",progress)],
]

def reaload():
    mods_setting_path = os.path.join(values["-folder_path-"],"setting.yml")

    # バグ対策してない、yml読み込み部分
    if os.path.isfile(mods_setting_path):
        with open(mods_setting_path,encoding="utf-8") as yml:
            yaml_data = yaml.safe_load(yml)

        for yml_key in need_key:
            if yml_key not in yaml_data.keys():
                sg.popup_error("setting.ymlが読み込めませんでした。\n必要な項目が足りていない可能性があります。")
                window["-title-"].Update("")
                window["-mod_version-"].Update("")
                window["-description-"].Update("")
                window["-assets_load-"].Update(disabled=True)
                window["-assets_unload-"].Update(disabled=True)
                window["-master_load-"].Update(disabled=True)
                window["-master_unload-"].Update(disabled=True)
                return
        window["-title-"].Update(yaml_data.get("title","情報がありません"))
        window["-mod_version-"].Update("mod_version : " + yaml_data.get("mod_version","情報がありません"))
        
        description_text = ""
        for description_line in yaml_data.get("description","情報がありません"):   
            description_text = description_text + description_line + "\n"
        if yaml_data.get("modloader_version") == modloader_version:
            window["-description-"].Update(description_text)
        else:
            window["-description-"].Update(description_text + "\n-Note-\nこのmodは\nmodloader_version : " + modloader_version + "\n向けのものです。")
    
        if os.path.isdir(os.path.join(values["-folder_path-"],"assets")):
            window["-assets_load-"].Update(disabled=False)
            window["-assets_unload-"].Update(disabled=False)

        if os.path.isdir(os.path.join(values["-folder_path-"],"master")):
            window["-master_load-"].Update(disabled=False)
            window["-master_unload-"].Update(disabled=False)

    else:
        window["-title-"].Update("")
        window["-mod_version-"].Update("")
        window["-description-"].Update("")
        window["-assets_load-"].Update(disabled=True)
        window["-assets_unload-"].Update(disabled=True)
        window["-master_load-"].Update(disabled=True)
        window["-master_unload-"].Update(disabled=True)

window = sg.Window("UmaMusume_Mod_Loader_GUI",layout)

while True:
    event,values = window.read()

    if event == "-folder_path-":
        reaload()

    if event == "-reload-":
        reaload()

    if event == "-assets_load-":
        popup_yesno = sg.popup_yes_no("本当にassetsをロードしますか？")
        if popup_yesno == "Yes":
            assets = os.listdir(os.path.join(values["-folder_path-"],"assets"))
            progress = 0

            window["-progress_bar-"].update(bar_color=("green4",""))
    
            for asset in assets:
                dat_asset_path = os.path.join(dat_path,asset[0:2],asset)
                mods_asset_path = os.path.join(values["-folder_path-"],"assets",asset)
                backup_asset_path = os.path.join(values["-folder_path-"],"backup",asset)

                # バックアップされてなかったら行う
                if os.path.isfile(dat_asset_path):
                    if not os.path.isfile(backup_asset_path):
                        shutil.copy(dat_asset_path,backup_asset_path)
                else:
                    sg.popup_error("datフォルダーに置き換え先のファイルが存在せず、バックアップが行えませんでした。\nウマ娘で「一括ダウンロード」をしてください \nassetsのロードを中断します。")
                    break

                # ロード
                shutil.copy(mods_asset_path,dat_asset_path)

                progress += 1
                window["-progress_value-"].update(F"assetsロード {progress} / {len(assets)} ")
                window["-progress_bar-"].update(max=len(assets),current_count=progress)
            sg.popup("assetsをロードしました。")
        else:
            sg.popup("assetsのロードを中断しました。")
    
    if event == "-assets_unload-":
        popup_yesno = sg.popup_yes_no("本当にassetsをアンロードしますか？")
        if popup_yesno == "Yes":
            assets = os.listdir(os.path.join(values["-folder_path-"],"assets"))
            progress = 0
            
            window["-progress_bar-"].update(bar_color=("red4",""))

            for asset in assets:
                dat_asset_path = os.path.join(dat_path,asset[0:2],asset)
                mods_asset_path = os.path.join(values["-folder_path-"],"assets",asset)
                backup_asset_path = os.path.join(values["-folder_path-"],"backup",asset)
                
                # ロード
                shutil.copy(backup_asset_path,dat_asset_path)
                
                progress += 1
                window["-progress_value-"].update(F"assetsアンロード {progress} / {len(assets)} ")
                window["-progress_bar-"].update(max=len(assets),current_count=progress)
            sg.popup("assetsをアンロードしました。")
        else:
            sg.popup("assetsのアンロードを中断しました。")

    if event == "-master_load-":
        popup_yesno = sg.popup_yes_no("本当にmasterをロードしますか？")
        if popup_yesno == "Yes":
            sql_path = os.path.join(values["-folder_path-"],"master","sql.txt")

            if os.path.isfile(sql_path):
                window["-progress_bar-"].update(bar_color=("green4",""))

                window["-progress_value-"].update("masterロード 0 / 1 ")
                window["-progress_bar-"].update(max=1,current_count=0)

                if os.path.isfile(master_path):
                    db = sqlite3.connect(master_path)
                    c = db.cursor()

                    with open(sql_path,mode="r",encoding="utf-8") as f:
                        c.executescript(f.read().replace("\n",""))

                    db.commit()

                    db.close()

                    window["-progress_value-"].update("masterロード 1 / 1 ")
                    window["-progress_bar-"].update(max=1,current_count=1)

                    sg.popup("masterをロードしました。")
                else:
                    sg.popup_error("master.mdbが存在しません。\n一度ウマ娘を起動してください。\nmasterのロードを中断します。")
            else:
                sg.popup_error("sql.txtが存在しません。\nmasterのロードを中断します。")
        else:
            sg.popup("masterのロードを中断しました。")

    if event == "-master_unload-":
        popup_yesno = sg.popup_yes_no("masterは仕様上、一部だけの解除が不可能であり、\n今まで読み込んだmasterのすべてがリセットされます。\nアンロードしたあとは、一度ウマ娘を起動してください。\n本当にmasterをアンロードしますか？")
        if popup_yesno == "Yes":
            window["-progress_bar-"].update(bar_color=("red4",""))

            window["-progress_value-"].update("masterアンロード 0 / 1 ")
            window["-progress_bar-"].update(max=1,current_count=0)

            if os.path.isfile(master_path):
                os.remove(master_path)

                window["-progress_value-"].update("masterアンロード 1 / 1 ")
                window["-progress_bar-"].update(max=1,current_count=1)

                sg.popup("masterをアンロードしました。\n一度ウマ娘を起動してください。")
            else:
                sg.popup_error("master.mdbが存在しません。\nすでにmasterがアンロードされています。\nmasterのアンロードを中断します。")
        else:
            sg.popup("masterのアンロードを中断しました。")
            
    if event == sg.WIN_CLOSED:
        break

window.close()