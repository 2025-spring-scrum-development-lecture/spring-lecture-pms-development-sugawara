import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime

class HotelBookingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("ホテル予約システム")
        self.root.geometry("700x800")  # 高さを少し増やす
        self.root.configure(bg="#f5f5f5")  # 背景色を設定
        
        # スタイル設定
        self.style = ttk.Style()
        self.style.configure("TFrame", background="#f5f5f5")
        self.style.configure("TLabel", background="#f5f5f5", font=("Helvetica", 10))
        self.style.configure("TButton", font=("Helvetica", 10, "bold"))
        self.style.configure("Header.TLabel", font=("Helvetica", 12, "bold"))
        self.style.configure("Price.TLabel", font=("Helvetica", 11, "bold"), foreground="#007bff")

        # 部屋の料金（1室あたりの料金）
        self.room_prices = {
            "岩手山展望露天風呂付き和室(本館)": 17400,
            "檜の内風呂本館和洋室(本館)": 18400,
            "岩手山側和室(本館)": 15400,
            "和室(本館)": 15400,
            "和室28畳(西館)": 15400,
            "和室10畳(西館)": 15400,
            "洋室10畳(西館)": 15400,
            "和洋室7.5畳(西館)": 15400
        }
        
        # 部屋の定員
        self.room_capacity = {
            "岩手山展望露天風呂付き和室(本館)": 5,
            "檜の内風呂本館和洋室(本館)": 5,
            "岩手山側和室(本館)": 5,
            "和室(本館)": 2,
            "和室28畳(西館)": 10,
            "和室10畳(西館)": 5,
            "洋室 ツイン(西館)": 2,
            "和洋室7.5畳(西館)": 5
        }
        
        self.banquet_price = 10000  # 宴会場の基本料金
        self.drink_price = 2800     # 飲み放題の一人あたり料金
        
        self.room_availability = {
            "岩手山展望露天風呂付き和室(本館)": 12,
            "檜の内風呂本館和洋室(本館)": 6,
            "岩手山側和室(本館)": 12,
            "和室(本館)": 3,
            "和室28畳(西館)": 1,
            "和室10畳(西館)": 3,
            "洋室10畳(西館)": 1,
            "和洋室7.5畳(西館)": 1
        }
        self.banquet_halls = ["春日", "平安", "末広", "芙蓉", "蘭", "桜", "岩鷲"]
        # 宴会場の予約状況を管理する辞書を追加
        self.banquet_reservations = {}
        self.reservations = []

        self.create_widgets()

    def create_widgets(self):
        # メインタイトル
        title_frame = ttk.Frame(self.root, style="TFrame")
        title_frame.pack(fill="x", padx=20, pady=10)
        
        title_label = ttk.Label(title_frame, text="ホテル予約システム", 
                               font=("Helvetica", 16, "bold"), background="#f5f5f5")
        title_label.pack()
        
        # コンテンツフレーム - 左側に入力フォーム、右側に料金情報
        content_frame = ttk.Frame(self.root, style="TFrame")
        content_frame.pack(fill="both", expand=True, padx=20, pady=5)
        
        # 左側 - 入力フォーム
        input_frame = ttk.LabelFrame(content_frame, text="予約情報", style="TFrame")
        input_frame.pack(side="left", fill="both", expand=True, padx=5, pady=5)
        
        # 予約ボタンセクション
        button_frame = ttk.Frame(self.root, style="TFrame")
        button_frame.pack(fill="x", padx=20, pady=10)
        
        self.book_button = ttk.Button(button_frame, text="予約する", command=self.book_room)
        self.book_button.pack(pady=10)
        
        # 予約リストセクション
        list_frame = ttk.LabelFrame(self.root, text="予約一覧", style="TFrame")
        list_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        # スクロールバー付きリストボックス
        scroll_frame = ttk.Frame(list_frame)
        scroll_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        scrollbar = ttk.Scrollbar(scroll_frame)
        scrollbar.pack(side="right", fill="y")
        
        self.reservations_listbox = tk.Listbox(scroll_frame, height=5, width=70, 
                                              font=("Helvetica", 9), bg="white",
                                              yscrollcommand=scrollbar.set)
        self.reservations_listbox.pack(side="left", fill="both", expand=True)
        scrollbar.config(command=self.reservations_listbox.yview)
