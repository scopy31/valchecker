import ctypes
import json
import os
import random
import tkinter
from tkinter import filedialog
from InquirerPy import inquirer
from InquirerPy.separator import Separator
import colorama
from PyQt5 import QtCore, QtGui, QtWidgets
import sys as syst




import requests

import checker
from codeparts.valkekerui.UI import Ui_MainWindow
from codeparts import checkers, systems, validsort
from codeparts.systems import system

check = checkers.checkers()
sys = systems.system()
valid = validsort.validsort()


class program():
    def __init__(self) -> None:
        self.count = 0
        self.checked = 0
        self.version = '4.0 beta'
        self.riotlimitinarow = 0
        path = os.getcwd()
        self.parentpath = os.path.abspath(os.path.join(path, os.pardir))
        try:
            self.lastver = requests.get(
                'https://api.github.com/repos/lil-jaba/valchecker/releases').json()[0]['tag_name']
        except:
            self.lastver = self.version

    def start(self):
        try:
            print('internet check')
            requests.get('https://github.com')
        except requests.exceptions.ConnectionError:
            print('no internet connection')
            os._exit(0)
        os.system('cls')
        app = QtWidgets.QApplication(syst.argv)
        MainWindow = QtWidgets.QMainWindow()
        ui = Ui_MainWindow()
        ui.setupUi(MainWindow)
        MainWindow.show()
        app.exec_()

    def get_accounts(self, filename):
        while True:
            try:
                with open(str(filename), 'r', encoding='UTF-8', errors='replace') as file:
                    lines = file.readlines()
                    # ret=list(set(lines))
                    ret = []
                    if len(lines) > 100000:
                        if inquirer.confirm(
                            message=f"You have more than 100k accounts ({len(lines)}). Do you want to skip the sorting part? (it removes doubles and bad logpasses but can be long)",
                            default=True,
                            qmark='!',
                            amark='!'
                        ).execute():
                            self.count = len(lines)
                            return lines

                    for logpass in lines:
                        logpass = logpass.split(' ')[0].replace(
                            '\n', '').replace(' ', '')
                        # remove doubles
                        if logpass not in ret and ':' in logpass:
                            self.count += 1
                            ctypes.windll.kernel32.SetConsoleTitleW(
                                f'ValChecker {self.version} by liljaba1337 | Loading Accounts ({self.count})')
                            ret.append(logpass)
                    return ret
            except FileNotFoundError:
                print(
                    f"can't find the default file ({filename})\nplease select a new one")
                root = tkinter.Tk()
                file = filedialog.askopenfile(parent=root, mode='rb', title='select file with accounts (login:password)',
                                              filetype=(("txt", "*.txt"), ("All files", "*.txt")))
                root.destroy()
                os.system('cls')
                if file == None:
                    print('you chose nothing')
                    input('press ENTER to choose again')
                    continue
                filename = str(file).split("name='")[1].split("'>")[0]
                with open('system\\settings.json', 'r+') as f:
                    data = json.load(f)
                    data['default_file'] = filename
                    f.seek(0)
                    json.dump(data, f, indent=4)
                    f.truncate()
                continue

    def main(self):
        ctypes.windll.kernel32.SetConsoleTitleW(
            f'ValChecker {self.version} by liljaba1337 | Loading Settings')
        print('loading settings')
        settings = sys.load_settings()

        ctypes.windll.kernel32.SetConsoleTitleW(
            f'ValChecker {self.version} by liljaba1337 | Loading Proxies')
        print('loading proxies')
        proxylist = sys.load_proxy()

        fn = settings['default_file']
        ctypes.windll.kernel32.SetConsoleTitleW(
            f'ValChecker {self.version} by liljaba1337 | Loading Accounts')
        print('loading accounts')
        accounts = self.get_accounts(fn)

        print('loading assets')
        ctypes.windll.kernel32.SetConsoleTitleW(
            f'ValChecker {self.version} by liljaba1337 | Loading Assets')
        sys.load_assets()

        print('loading checker')
        ctypes.windll.kernel32.SetConsoleTitleW(
            f'ValChecker {self.version} by liljaba1337 | Loading Checker')
        scheck = checker.simplechecker(settings, proxylist, self.version)
        scheck.main(accounts, self.count)
        return


pr = program()
if __name__ == '__main__':
    print('starting')
    pr.start()
