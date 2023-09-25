import webbrowser
import requests
from PyQt5.QtWidgets import QMessageBox

UPDATE_URL = "https://raw.githubusercontent.com/coolyer/CoolyerScraperUI/main/version.txt"  # URL where the latest version information is available
def read_version():
    try:
        with open("version.txt", "r") as file:
            version = file.read().strip()
        return version
    except FileNotFoundError:
        print("Could not find version.txt in the current working directory grabbing latest version from github")
        # Handle the missing file by creating it
        try:
            response = requests.get(UPDATE_URL)
            latestv = response.text.strip()
            with open("version.txt", "w") as file:
                file.write(latestv)
            return latestv
        except Exception as e:
            print(None, 'Error', f"An error occurred while checking for updates: {str(e)}")
            return None  # Handle the error as needed
CURRENT_VERSION = read_version()

def check_for_updates(parent_widget):
        try:
                response = requests.get(UPDATE_URL)
                latest_version = response.text.strip()
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
                if CURRENT_VERSION > latest_version:
                    msg = QMessageBox()
                    msg.setIcon(QMessageBox.Information)
                    msg.setWindowTitle("Information")
                    msg.setText(f'Whoopsie-doodle! Looks like someone could not resist playing with version.txt. 😄Just so you know, youre currently strutting your stuff with this version: {CURRENT_VERSION}. Keep it cool and scrape on!\n Latest version is: {latest_version}')
                    msg.setStandardButtons(QMessageBox.Ok)
                    msg.exec_()
        except Exception as e:
            QMessageBox.critical(parent_widget, 'Error', f"An error occurred while checking for updates: {str(e)}")
        
def version_check(parent_widget):
    try:    
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setWindowTitle("Information")
        msg.setText(f'You are using version:\n{CURRENT_VERSION}')
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec_()
    except Exception as e:
            QMessageBox.critical(parent_widget, 'Error', f"An error occurred while checking for updates: {str(e)}")