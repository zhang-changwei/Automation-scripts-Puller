import json
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox
from main import *
import os

class App:

    def __init__(self):
        self.root = tk.Tk()
        self.root.title('Automation scripts Puller')
        self.root.protocol('WM_DELETE_WINDOW', self.close)

        self.loadConfig()

        # frame 1
        self.autoloadVar = tk.StringVar(value=self.config['local'])
        frame1 = tk.Frame(self.root)
        frame1.pack(side='top', fill='x', padx=5, pady=5)
        ttk.Button(frame1, text='Select autoload folder', command=self.setLocalFolder) \
            .pack(side='left', padx=2, pady=2)
        ttk.Entry(frame1, state='readonly', textvariable=self.autoloadVar, width=40) \
            .pack(side='left', padx=2, pady=2)

        # frame 2
        self.remote = getRemoteInfos(url=self.config['remote'])

        self.checks:list[tk.BooleanVar] = []
        self.cmps:list[tk.StringVar] = []

        frame2 = tk.Frame(self.root)
        frame2.pack(side='top', fill='x', padx=5, pady=(0, 5))
        i = 0
        for name, v in self.remote.items():
            localVersion = None
            remoteVersion = v['version']
            if os.path.exists(self.autoloadVar.get()):
                local = os.path.join(self.autoloadVar.get(), name + '.lua')
                if os.path.exists(local):
                    localVersion = getLocalVersion(local)
            cmp = str(localVersion) + ' -> ' + remoteVersion
            checkVar = tk.BooleanVar(value=False)
            cmpVar = tk.StringVar(value=cmp)
            ttk.Checkbutton(frame2, text=name, variable=checkVar) \
                .grid(row=i, column=0, padx=2, pady=2, sticky='w')
            ttk.Label(frame2, textvariable=cmpVar) \
                .grid(row=i, column=1, padx=2, pady=2, sticky='w')

            self.checks.append(checkVar)
            self.cmps.append(cmpVar)
            i += 1

        # frame 3
        frame3 = tk.Frame(self.root)
        frame3.pack(side='top', fill='x', padx=5, pady=(0, 5))
        ttk.Button(frame3, text='Update', command=self.run).pack()
        # frmae 4
        frame4 = tk.Frame(self.root)
        frame4.pack(side='top', fill='x', padx=5, pady=(0, 5))
        note = '''1. 使用本程序时请保持开启魔法上网，以正常拉取脚本。\n2. 若Aegisub安装目录在C盘，请使用管理员身份运行此软件。'''
        ttk.Label(frame4, text=note, justify='left') \
            .pack(side='left', padx=2, pady=2)

        self.root.mainloop()

    def run(self):
        assert(self.autoloadVar.get() != '' and os.path.exists(self.autoloadVar.get()))
        for name, v, checkVar, cmpVar in zip(self.remote.keys(), self.remote.values(), self.checks, self.cmps):
            if checkVar.get():
                success, script = pullRemoteScripts(v['url'])
                if success:
                    local = os.path.join(self.autoloadVar.get(), name + '.lua')
                    with open(local, 'wb') as f:
                        f.write(script.read())
                        checkVar.set(False)
                        cmpVar.set(v['version'] + ' -> ' + v['version'])
        messagebox.showinfo(title='Update', message='Success!')

    def setLocalFolder(self):
        fp = filedialog.askdirectory(title='set autoload folder')
        if fp:
            self.autoloadVar.set(fp)
            for name, cmpVar in zip(self.remote.keys(), self.cmps):
                local = os.path.join(self.autoloadVar.get(), name + '.lua')
                if os.path.exists(local):
                    localVersion = getLocalVersion(local)
                    cmp = localVersion + ' -> ' + cmpVar.get().split(' -> ')[-1]
                    cmpVar.set(cmp)

    def loadConfig(self):
        with open('config.json') as f:
            self.config = json.load(f)
    def writeConfig(self):
        self.config['local'] = self.autoloadVar.get()
        with open('config.json', 'w') as f:
            json.dump(self.config, f, indent=4)

    def close(self):
        self.writeConfig()
        self.root.destroy()

if __name__ == '__main__':
    App()