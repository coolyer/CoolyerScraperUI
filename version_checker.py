import webbrowser
import requests
from PyQt5.QtWidgets import QMessageBox

def read_version():
    try:
        with open("version.txt", "r") as file:
            version = file.read().strip()
        return version
    except FileNotFoundError:
        print("version.txt not found. Using default version '1.0'")
        return "1.0"
CURRENT_VERSION = read_version()
UPDATE_URL = "https://raw.githubusercontent.com/coolyer/CoolyerScraperUI/main/version.txt"  # URL where the latest version information is available

def check_for_updates(parent_widget):
        try:
                response = requests.get(UPDATE_URL)
                latest_version = response.text.strip()
                print(latest_version)
                if latest_version > CURRENT_VERSION:
                    message = f"A new version is available ({latest_version}). Do you want to update?\nYou are using version {read_version()}"
                    reply = QMessageBox.question(parent_widget,'Update Available', message, QMessageBox.Yes | QMessageBox.No)
                    
                    if reply == QMessageBox.Yes:
                        github_url = 'https://github.com/coolyer/CoolyerScraperUI/releases'
                        webbrowser.open(github_url)
                if latest_version == CURRENT_VERSION:
                    msg = QMessageBox()
                    msg.setIcon(QMessageBox.Information)
                    msg.setWindowTitle("Information")
                    msg.setText(f'CoolyerScraper is up to date.\nYou are using version:\n{CURRENT_VERSION}')
                    msg.setStandardButtons(QMessageBox.Ok)
                    msg.exec_()
        except Exception as e:
            QMessageBox.critical(parent_widget, 'Error', f"An error occurred while checking for updates: {str(e)}")
            
def version_check():
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Information)
    msg.setWindowTitle("Information")
    msg.setText(f'You are using version:\n{CURRENT_VERSION}')
    msg.setStandardButtons(QMessageBox.Ok)
    msg.exec_()