from tkinter import *
from datetime import datetime
import tkinter.messagebox as messagebox
from datetime import timedelta
import csv
import os

class Application(Frame):
    def __init__(self, root = None):
        super().__init__(root, width = 500, height=350,
                         borderwidth=1, relief = 'groove')
        self.root = root
        self.pack()
        self.pack_propagate(0)
        self.create_widgets()

    def create_widgets(self):
        text_date = Label(self, text = "日付(yyyy-mm-dd)")
        text_inventory = Label(self, text = "在庫(数値を指定)")
        text_fileName = Label(self, text = "ファイル名(拡張子を付けない)")
        #日付を入力されるテキストエリア
        self.input_date_area = Entry(self)

        #在庫を入力されるテキストエリア
        self.input_inventory_area = Entry(self)

        #ファイル名を入力されるテキストエリア
        self.input_fileName_area = Entry(self)

        #CVSファイル出力ボタン
        registration_button = Button(
            self,
            text="CVSファイルに出力",
            border = 1,
            width=15,
            command=self.registration
        )
        #ここでウィジェットを配置
        text_date.place(x = 20, y = 15)
        text_inventory.place(x = 20, y = 45)
        text_fileName.place(x = 20, y = 75)
        self.input_date_area.place(x = 170, y = 17)
        self.input_inventory_area.place(x = 170, y = 47)
        self.input_fileName_area.place(x = 170, y = 77)
        registration_button.place(x = 340, y = 75)

    #CVSファイル出力ボタンを押したときの処理
    def registration(self):
        try:
            date = datetime.strptime(self.input_date_area.get(), '%Y-%m-%d').date()
            inventory = int(self.input_inventory_area.get())
            fileName = self.input_fileName_area.get()
        except ValueError:
            messagebox.showwarning("警告","入力が間違っています。")

        if "." in fileName or inventory == 0:
                messagebox.showwarning("警告", "在庫に0が入力またはファイル名に拡張子が付いています。")
        else :
            result_Gnar = [[0]*5 for i in range(inventory + 1)] #コンタクトの期限を格納する配列
            result_Gnar[0][0] = "開始日"
            result_Gnar[0][3] = "終了日"
            result_Gnar[0][1] = " "
            result_Gnar[0][2] = " "
            result_Gnar[0][4] = " "

            #コンタクトの期限を計算する処理
            for cnt in range(inventory):
                result_Gnar[cnt + 1][2] = " "
                result_Gnar[cnt + 1][0] = str(date.year) + "年"
                result_Gnar[cnt + 1][1] = str(date.month) + "月" + str(date.day) + "日"
                date = date + timedelta(days = 13)
                result_Gnar[cnt + 1][3] = str(date.year) + "年"
                result_Gnar[cnt + 1][4] = str(date.month) + "月" + str(date.day) + "日"
                date = date + timedelta(days = 1)

            # CSVファイルに書き込む
            desktop_path = os.path.join(os.path.expanduser("~"), "OneDrive\デスクトップ\コンタクトレンズ期間")
            file_path = os.path.join(desktop_path, fileName + ".csv")
            with open(file_path, "w", encoding="utf-8_sig") as file:
                writer = csv.writer(file, delimiter=',', quoting=csv.QUOTE_MINIMAL)
                writer.writerows(result_Gnar)

root = Tk()
root.title("コンタクト、次いつ変える?")
root.geometry("500x350")
root.resizable(0, 0)
app = Application(root = root)
root.mainloop()
