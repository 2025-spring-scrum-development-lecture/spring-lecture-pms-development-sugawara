import tkinter as tk
from tkinter import ttk

def setup_styles():
    """アプリケーション全体のスタイルを設定"""
    style = ttk.Style()
    style.configure("TFrame", background="#f5f5f5")
    style.configure("TLabel", background="#f5f5f5", font=("Helvetica", 10))
    style.configure("TButton", font=("Helvetica", 10, "bold"))
    style.configure("Header.TLabel", font=("Helvetica", 12, "bold"))
    style.configure("Price.TLabel", font=("Helvetica", 11, "bold"), foreground="#007bff")
    return style

def create_title_section(parent):
    """タイトルセクションを作成"""
    title_frame = ttk.Frame(parent, style="TFrame")
    title_frame.pack(fill="x", padx=20, pady=10)
    
    title_label = ttk.Label(title_frame, text="ホテル予約システム", 
                           font=("Helvetica", 16, "bold"), background="#f5f5f5")
    title_label.pack()
    return title_frame

def create_customer_section(parent):
    """顧客情報セクションを作成"""
    customer_frame = ttk.Frame(parent, style="TFrame")
    customer_frame.pack(fill="x", padx=10, pady=5)
    
    ttk.Label(customer_frame, text="顧客情報", style="Header.TLabel").grid(row=0, column=0, columnspan=2, sticky="w", pady=(5,10))
    
    ttk.Label(customer_frame, text="名前:").grid(row=1, column=0, sticky="w", padx=5, pady=5)
    name_entry = ttk.Entry(customer_frame, width=30)
    name_entry.grid(row=1, column=1, sticky="w", padx=5, pady=5)

    ttk.Label(customer_frame, text="メール:").grid(row=2, column=0, sticky="w", padx=5, pady=5)
    email_entry = ttk.Entry(customer_frame, width=30)
    email_entry.grid(row=2, column=1, sticky="w", padx=5, pady=5)
    
    return customer_frame, name_entry, email_entry

def create_stay_section(parent, room_types):
    """宿泊情報セクションを作成"""
    from tkcalendar import DateEntry
    
    stay_frame = ttk.Frame(parent, style="TFrame")
    stay_frame.pack(fill="x", padx=10, pady=5)
    
    ttk.Label(stay_frame, text="宿泊情報", style="Header.TLabel").grid(row=0, column=0, columnspan=2, sticky="w", pady=(10,5))

    ttk.Label(stay_frame, text="チェックイン日:").grid(row=1, column=0, sticky="w", padx=5, pady=5)
    checkin_entry = DateEntry(stay_frame, width=15, background='darkblue', foreground='white', borderwidth=2)
    checkin_entry.grid(row=1, column=1, sticky="w", padx=5, pady=5)
    
    ttk.Label(stay_frame, text="チェックアウト日:").grid(row=2, column=0, sticky="w", padx=5, pady=5)
    checkout_entry = DateEntry(stay_frame, width=15, background='darkblue', foreground='white', borderwidth=2)
    checkout_entry.grid(row=2, column=1, sticky="w", padx=5, pady=5)

    ttk.Label(stay_frame, text="部屋の種類:").grid(row=3, column=0, sticky="w", padx=5, pady=5)
    room_type = ttk.Combobox(stay_frame, values=list(room_types), state="readonly", width=30)
    room_type.grid(row=3, column=1, sticky="w", padx=5, pady=5)

    ttk.Label(stay_frame, text="人数:").grid(row=4, column=0, sticky="w", padx=5, pady=5)
    num_people = ttk.Combobox(stay_frame, values=[], state="readonly", width=10)
    num_people.grid(row=4, column=1, sticky="w", padx=5, pady=5)
    
    return stay_frame, checkin_entry, checkout_entry, room_type, num_people

def create_banquet_section(parent):
    """宴会オプションセクションを作成"""
    banquet_frame = ttk.Frame(parent, style="TFrame")
    banquet_frame.pack(fill="x", padx=10, pady=5)
    
    ttk.Label(banquet_frame, text="宴会オプション", style="Header.TLabel").grid(row=0, column=0, columnspan=2, sticky="w", pady=(10,5))
    
    banquet_var = tk.BooleanVar()
    banquet_check = ttk.Checkbutton(banquet_frame, text="宴会場を予約する (10,000円追加)", 
                                  variable=banquet_var)
    banquet_check.grid(row=1, column=0, columnspan=2, sticky="w", padx=5, pady=5)

    banquet_choice_label = ttk.Label(banquet_frame, text="宴会場選択:")
    banquet_choice_label.grid(row=2, column=0, sticky="w", padx=5, pady=5)
    banquet_choice = ttk.Combobox(banquet_frame, values=[], state="disabled", width=15)
    banquet_choice.grid(row=2, column=1, sticky="w", padx=5, pady=5)
    
    # 飲み放題オプション
    drinks_var = tk.BooleanVar()
    drinks_check = ttk.Checkbutton(banquet_frame, text="飲み放題オプション (一人2,800円追加)", 
                                 variable=drinks_var, state="disabled")
    drinks_check.grid(row=3, column=0, columnspan=2, sticky="w", padx=5, pady=5)
    
    return banquet_frame, banquet_var, banquet_check, banquet_choice, banquet_choice_label, drinks_var, drinks_check

def create_price_section(parent):
    """料金情報セクションを作成"""
    price_frame = ttk.LabelFrame(parent, text="料金情報", style="TFrame")
    price_frame.pack(side="right", fill="both", expand=True, padx=5, pady=5)
    
    price_info_frame = ttk.Frame(price_frame, style="TFrame")
    price_info_frame.pack(fill="x", padx=10, pady=10)
    
    ttk.Label(price_info_frame, text="宿泊日数:").grid(row=0, column=0, sticky="w", padx=5, pady=5)
    nights_label = ttk.Label(price_info_frame, text="-", style="Price.TLabel")
    nights_label.grid(row=0, column=1, sticky="w", padx=5, pady=5)

    ttk.Label(price_info_frame, text="合計料金:").grid(row=1, column=0, sticky="w", padx=5, pady=5)
    price_label = ttk.Label(price_info_frame, text="-", style="Price.TLabel")
    price_label.grid(row=1, column=1, sticky="w", padx=5, pady=5)

    ttk.Label(price_info_frame, text="料金内訳:").grid(row=2, column=0, sticky="w", padx=5, pady=5)
    price_details = ttk.Label(price_info_frame, text="-", wraplength=250)
    price_details.grid(row=3, column=0, columnspan=2, sticky="w", padx=5, pady=5)
    
    return price_frame, nights_label, price_label, price_details

def create_button_section(parent):
    """予約ボタンセクションを作成"""
    button_frame = ttk.Frame(parent, style="TFrame")
    button_frame.pack(fill="x", padx=20, pady=10)
    
    book_button = ttk.Button(button_frame, text="予約する")
    book_button.pack(pady=10)
    
    return button_frame, book_button

def create_reservation_list(parent):
    """予約リストセクションを作成"""
    list_frame = ttk.LabelFrame(parent, text="予約一覧", style="TFrame")
    list_frame.pack(fill="both", expand=True, padx=20, pady=10)
    
    # スクロールバー付きリストボックス
    scroll_frame = ttk.Frame(list_frame)
    scroll_frame.pack(fill="both", expand=True, padx=10, pady=10)
    
    scrollbar = ttk.Scrollbar(scroll_frame)
    scrollbar.pack(side="right", fill="y")
    
    reservations_listbox = tk.Listbox(scroll_frame, height=5, width=70, 
                                    font=("Helvetica", 9), bg="white",
                                    yscrollcommand=scrollbar.set)
    reservations_listbox.pack(side="left", fill="both", expand=True)
    scrollbar.config(command=reservations_listbox.yview)
    
    return list_frame, reservations_listbox