import tkinter as tk
import tkinter.messagebox as tm
from tkinter import *

from controller import action_Run


USERNAME = 'xxx'
PASSWORD = 'xxx'

# 弹窗
class MyDialog(tk.Toplevel):
    def __init__(self):
        super().__init__()
        self.title('登录界面')
        self.geometry("+450+300")
        # 弹窗界面
        self.userinfo = None
        # 不在这里加 self.userinfo = None 会导致弹窗点x关闭报错
        self.setup_UI()

    def setup_UI(self):
        # 第一行（两列）
        row1 = tk.Frame(self)
        row1.pack(fill="x")
        tk.Label(row1, text='用户名：', width=8).pack(side=tk.LEFT)
        self.name = tk.StringVar()
        e1 = tk.Entry(row1 ,textvariable=self.name, width=20)
        e1.insert(END,USERNAME)
        e1.pack(side=tk.LEFT)

        # 第二行
        row2 = tk.Frame(self)
        row2.pack(fill="x", ipadx=1, ipady=1)
        tk.Label(row2, text='密码：', width=8).pack(side=tk.LEFT)
        self.password = tk.StringVar()
        e2 = tk.Entry(row2, textvariable=self.password, width=20,show="*")
        e2.insert(END,PASSWORD)
        e2.pack(side=tk.LEFT)

        # 第三行
        row3 = tk.Frame(self)
        row3.pack(fill="x")
        tk.Button(row3, text="取消", command=self.cancel).pack(side=tk.RIGHT)
        tk.Button(row3, text="确定", command=self.ok).pack(side=tk.RIGHT)

    def ok(self):
        self.userinfo = [self.name.get(), self.password.get()]  # 设置数据
        if self.userinfo[0] == USERNAME and self.userinfo[1] == PASSWORD:
            tm.showinfo(title='tip', message='登录成功')
            self.destroy()  # 销毁窗口
        else:
            tm.showinfo(title='tip', message='用户名或密码错误，请重试！')


    def cancel(self):
        self.userinfo = None  # 空！
        self.destroy()

# 主窗
class MyApp(tk.Tk):
    def __init__(self):
        super().__init__()
        # self.pack() # 若继承 tk.Frame ，此句必须有！
        self.title('爬虫界面')
        self.geometry("+500+350")

        # 程序参数/数据
        self.name = ''
        self.password = ''

        # 程序界面
        self.setupUI()

    def setupUI(self):
        # 第一行（两列）
        row1 = tk.Frame(self)
        row1.pack(fill="x")
        tk.Label(row1, text='状态：', width=8).pack(side=tk.LEFT)
        self.l1 = tk.Label(row1, text="未登录", width=40)
        self.l1.pack(side=tk.LEFT)

        # 第二行
        row2 = tk.Frame(self)
        row2.pack(fill="x")
        tk.Label(row2, text='提示：', width=8).pack(side=tk.LEFT)
        self.l2 = tk.Label(row2, text="您还未登录，请点击登录", width=40)
        self.l2.pack(side=tk.LEFT)

        #第三行
        row3 = tk.Frame(self)
        row3.pack(fill="x")
        bm = PhotoImage(file = '360security.png')
        tk.Label(row3, image = bm,text = '图片').pack()
        tk.Label.bm = bm

        # 第四行
        row4 = tk.Frame(self)
        row4.pack(fill="x")
        tk.Button(row4, text="登录", command=self.setup_config).pack(side=tk.RIGHT)
        tk.Button(row4, text="开始", command=self.steup_Run).pack(side=tk.LEFT)

    # 设置参数
    def setup_config(self):
        # 接收弹窗的数据
        res = self.ask_userinfo()
        if res is None:
            return
        # 更改参数
        self.name, self.password = res

        # 更新界面
        if self.name == USERNAME and self.password == PASSWORD:
            self.l1.config(text=self.name + " 已登录" )
            self.l2.config(text="您已登录成功，可以点击 开始 进行爬虫")

    # 弹窗
    def ask_userinfo(self):
        if self.name == USERNAME and self.password == PASSWORD:
            tm.showinfo(title='tip', message='您已登录')
            return
        inputDialog = MyDialog()
        self.wait_window(inputDialog)  # 这一句很重要！！！
        return inputDialog.userinfo

    def steup_Run(self):

        if self.name == USERNAME and self.password == PASSWORD:
            self.destroy()
            action_Run.action_Run()

        else:
            tm.showinfo(title='tip', message='您未登录，请登录')

if __name__ == '__main__':
    app = MyApp()
    app.mainloop()