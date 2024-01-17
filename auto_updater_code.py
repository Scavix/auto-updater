import requests
import PySimpleGUI as sg
import subprocess
import os

version = "1.0.0"

def main():
    layout = [[sg.Button('Generate Source'), sg.Button('Build Script'), sg.Button('Check update'), sg.Button('Exit')]]

    window = sg.Window('Auto updater ' + version, layout,
                       element_justification='c', finalize=True)

    try:
        while True:
            event, values = window.read()
            if event == 'Exit' or event == sg.WIN_CLOSED:
                break
            elif event == 'Generate Source':
                if download_source():
                    sg.popup("Done")
                else:
                    sg.popup("Web site does not exist or is not reachable")
            elif event == 'Build Script':
                if download_build_script():
                    sg.popup("Done")
                else:
                    sg.popup("Web site does not exist or is not reachable")
            elif event == 'Check update':
                response = requests.get("https://raw.githubusercontent.com/Scavix/auto-updater/main/version.json")
                if response.status_code == 200:
                    if response.json()["version"] != version:
                        if sg.popup_yes_no("New version available: " + response.json()["version"] + ". Do you want to update?", title="To update") == "Yes":
                            if download_both():
                                subprocess.run([r"auto_updater_build_script.bat"])
                                os.remove("auto_updater_code.py")
                                os.remove("auto_updater_build_script.bat")
                                os.remove("auto_updater_code.spec")
                                sg.popup("Done")
                                window.close()
                            else:
                                sg.popup("Web site does not exist or is not reachable")
                            break
                    else:
                        sg.popup("No new version available, actual: " + response.json()["version"], title="Updated")
                else:
                    sg.popup("Web site does not exist or is not reachable\n" +
                             response.status_code+"\n"+response.reason+"\n"+response.text)
    except:
        sg.popup("Found exception, closing...")
    window.close()

def download_source():
    response = requests.get(
        "https://raw.githubusercontent.com/Scavix/auto-updater/main/auto_updater_code.py")
    if response.status_code == 200:
        f = open("auto_updater_code.py", "w")
        f.write(response.text)
        f.close()
        return True
    else:
        return False

def download_build_script():
    response = requests.get(
        "https://raw.githubusercontent.com/Scavix/auto-updater/main/auto_updater_build_script.bat")
    if response.status_code == 200:
        f = open("auto_updater_build_script.bat", "w")
        f.write(response.text)
        f.close()
        return True
    else:
        return False

def download_both():
    res1=download_source()
    res2=download_build_script()
    if res1 and res2:
        return True
    else:
        if res1:
            os.remove("auto_updater_code.py")
        if res2:
            os.remove("auto_updater_build_script.bat")
        return False

if __name__ == "__main__":
    main()
