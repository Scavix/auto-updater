import requests
import PySimpleGUI as sg
import subprocess

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
                download_source()
            elif event == 'Build Script':
                download_build_script()
            elif event == 'Check update':
                response = requests.get("https://raw.githubusercontent.com/Scavix/auto-updater/main/version.json")
                if response.status_code == 200:
                    if response.json()["version"] != version:
                        if sg.popup_yes_no("New version available: " + response.json()["version"] + ". Do you want to update?", title="To update") == "Yes":
                            download_source()
                            download_build_script()
                            subprocess.run([r"auto_updater_build_script.bat"])
                            sg.popup("Done")
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
        sg.popup("Done")
    else:
        sg.popup("Web site does not exist or is not reachable")

def download_build_script():
    response = requests.get(
        "https://raw.githubusercontent.com/Scavix/auto-updater/main/auto_updater_build_script.bat")
    if response.status_code == 200:
        f = open("auto_updater_build_script.bat", "w")
        f.write(response.text)
        f.close()
        sg.popup("Done")
    else:
        sg.popup("Web site does not exist or is not reachable")

if __name__ == "__main__":
    main()
