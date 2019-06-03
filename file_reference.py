import os,sys
import tkinter as Tk

from tkinter import filedialog
from tkinter import messagebox

class Application(Tk.Frame):
    def __init__(self, master=None):
        Tk.Frame.__init__(self, master)
        self.master.title("初期設定画面")
        self.master.geometry("600x200")
        self.pack()
        self.create_widgets()

    # 参照ボタン押下時の定義
    def button1_clicked(self):
        #生データディレクトリ data をカレントディレクトリとする。
        os.chdir("./data")
        fTyp = [("","*")]
        iDir = os.path.abspath(os.path.dirname(__file__))
        FilePath = filedialog.askopenfilename(filetypes = fTyp,initialdir = iDir)
        SelectedFile = os.path.basename(FilePath)
        self.File1.set(SelectedFile)

    # Okボタン押下時の定義
    #def button2_clicked(self):

    # ウィジェットの定義
    def create_widgets(self):
        # 解析対象ファイル レーベル
        self.label1 = Tk.Label(self, text = u'解析対象のファイル')
        # 選択した解析対象ファイルの表示
        self.File1 = Tk.StringVar()
        self.File1_entry = Tk.Entry(self, textvariable = self.File1, width = 50)
        # 参照ボタンの作成
        self.button1 = Tk.Button(self, text=u'参照', command = self.button1_clicked)

        # 風量設定 レーベル
        self.label2 = Tk.Label(self, text = u'解析条件の風量を入力してください')
        # 風量設定 エントリー
        self.AirVolume_entry = Tk.Entry(self, width = 50)
        # 風量設定 レーベル
        self.label3 = Tk.Label(self, text = u'm3/hr')

        # 特記事項設定 レーベル
        self.label4 = Tk.Label(self, text = u'特記事項を入力してください')
        # 特記事項設定 エントリー
        self.Notices_entry = Tk.Entry(self, width = 50)

        self.label1.grid(column=0, row=0)
        self.File1_entry.grid(column=0, row=1)
        self.button1.grid(column=1, row=1)

        self.label2.grid(column=0, row=2)
        self.AirVolume_entry.grid(column=0, row=3)
        self.label3.grid(column=1, row=3)

        self.label4.grid(column=0, row=4)
        self.Notices_entry.grid(column=0, row=5)

# main
if __name__ == '__main__':
    root = Tk.Tk()
    app = Application(master=root)
    app.mainloop()
























'''
# 参照ボタンのイベント
# button1クリック時の処理
def button1_clicked():
    fTyp = [("","*")]
    iDir = os.path.abspath(os.path.dirname(__file__))
    FilePath = filedialog.askopenfilename(filetypes = fTyp,initialdir = iDir)
    SelectedFilePath.set(FilePath)

# button2クリック時の処理
def button2_clicked():
    messagebox.showinfo('FileReference Tool', u'参照ファイルは↓↓\n' + file1.get())

def root():
    root = tkinter()
    root.title('FileReference Tool')
    root.resizable(False, False)

    # Frame1の作成
    frame1 = ttkinter.Frame(root, padding=10)
    frame1.grid()

    # 参照ボタンの作成
    button1 = ttkinter.Button(root, text=u'参照', command=button1_clicked)
    button1.grid(row=0, column=3)

    # ラベルの作成
    # 「ファイル」ラベルの作成
    s = StringVar()
    s.set('ファイル>>')
    label1 = ttkinter.Label(frame1, textvariable=s)
    label1.grid(row=0, column=0)

    # 参照ファイルパス表示ラベルの作成
    file1 = StringVar()
    file1_entry = ttkinter.Entry(frame1, textvariable=file1, width=50)
    file1_entry.grid(row=0, column=2)

    # Frame2の作成
    frame2 = ttkinter.Frame(root, padding=(0,5))
    frame2.grid(row=1)

    # Startボタンの作成
    button2 = ttkinter.Button(frame2, text='Start', command=button2_clicked)
    button2.pack(side=LEFT)

    # Cancelボタンの作成
    button3 = ttkinter.Button(frame2, text='Cancel', command=quit)
    button3.pack(side=LEFT)

    root.mainloop()
'''
