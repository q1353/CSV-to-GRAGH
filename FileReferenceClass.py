import os,sys
import tkinter as Tk

from tkinter import filedialog
from tkinter import messagebox

class Application(Tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.master.title("初期設定画面")
        self.master.geometry("600x200")
        self.pack()
        self.create_widgets()

    # 参照ボタン押下時の定義
    def button1_clicked(self):
        #生データディレクトリ data をカレントディレクトリとする。
        #os.chdir("./data")
        fTyp = [("","*")]
        iDir = os.path.abspath(os.path.dirname(__file__))
        FilePath = filedialog.askopenfilename(filetypes = fTyp,initialdir = iDir)
        self.SelectedFile = os.path.basename(FilePath)
        self.File1.set(self.SelectedFile)

    # Okボタン押下時の定義
    def button2_clicked(self):
        # 参照ファイルの出力（ゲット）
        self.SelectFile = self.File1_entry.get()
        # 風量設定の出力（ゲット）
        self.AirVolume = self.AirVolume_entry.get()
        # 特記事項の出力（ゲット）
        self.Notices = self.Notices_entry.get()

        if len (self.SelectFile) == 0 :
            messagebox.showwarning('WARNING', u'解析対象ファイルが選択してください。')
        elif len (self.AirVolume) == 0 :
            messagebox.showwarning('WARNING', u'風量の初期設定を行ってください。')
        else :
            msgcheck = messagebox.askokcancel('最終確認', u'この設定で良いですか？\n参照ファイル >>>' + self.SelectFile + '\n風量の初期設定 >>>' + self.AirVolume + '\n特記事項 >>>' + self.Notices)
            if msgcheck == 1:
                self.quit()
                self.destroy()

    # ウィジェットの定義
    def create_widgets(self):
        # 解析対象ファイル レーベル
        self.label1 = Tk.Label(self, text = u'解析対象のファイルを選択してください。')
        # 選択した解析対象ファイルの表示
        self.File1 = Tk.StringVar()
        self.File1_entry = Tk.Entry(self, textvariable = self.File1, width = 50)
        # 参照ボタンの作成
        self.button1 = Tk.Button(self, text=u'参照', command = self.button1_clicked, width = 10)

        # 風量設定 レーベル
        self.label2 = Tk.Label(self, text = u'解析条件の風量を入力してください。')
        # 風量設定 エントリー
        self.AirVolume_entry = Tk.Entry(self, width = 50)
        # 風量設定 レーベル
        self.label3 = Tk.Label(self, text = u'm3/hr')

        # 特記事項設定 レーベル
        self.label4 = Tk.Label(self, text = u'特記事項を入力してください。')
        # 特記事項設定 エントリー
        self.Notices_entry = Tk.Entry(self, width = 50)

        # 参照ボタンの作成
        self.button2 = Tk.Button(self, text=u'OK', command = self.button2_clicked, width = 10)


        # ダイアログ表示設定
        self.label1.grid(column=0, row=0)
        self.File1_entry.grid(column=0, row=1)
        self.button1.grid(column=2, row=1)

        self.label2.grid(column=0, row=2)
        self.AirVolume_entry.grid(column=0, row=3)
        self.label3.grid(column=2, row=3)

        self.label4.grid(column=0, row=4)
        self.Notices_entry.grid(column=0, row=5)

        self.button2.grid(column=0, row=7)


def main ():
    root = Tk.Tk()
    app = Application(master=root)
    app.mainloop()
    return app.SelectFile, app.AirVolume, app.Notices

# main
if __name__ == '__main__':
    main ()
