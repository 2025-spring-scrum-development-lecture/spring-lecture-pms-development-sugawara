import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import json
from models import RoomModel, BanquetModel, ReservationData
from utils import calculate_nights, send_confirmation_email, format_reservation_text
import ui_components

class HotelBookingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("ホテル予約システム")
        self.root.geometry("700x800")
        self.root.configure(bg="#f5f5f5")
        
        # モデルの初期化
        self.room_model = RoomModel()
        self.banquet_model = BanquetModel()
        self.reservation_data = ReservationData()
        
        # スタイルの設定
        self.style = ui_components.setup_styles()
        
        # UI構築
        self.create_widgets()
        
    def create_widgets(self):
        # メインタイトル
        ui_components.create_title_section(self.root)
        
        # コンテンツフレーム
        content_frame = ttk.Frame(self.root, style="TFrame")
        content_frame.pack(fill="both", expand=True, padx=20, pady=5)
        
        # 左側 - 入力フォーム
        input_frame = ttk.LabelFrame(content_frame, text="予約情報", style="TFrame")
        input_frame.pack(side="left", fill="both", expand=True, padx=5, pady=5)
        
        # 顧客情報
        customer_section, self.name_entry, self.email_entry = ui_components.create_customer_section(input_frame)
        
        # 宿泊情報
        stay_section, self.checkin_entry, self.checkout_entry, self.room_type, self.num_people = ui_components.create_stay_section(
            input_frame, self.room_model.room_prices.keys()
        )
        
        # イベントバインド
        self.checkin_entry.bind("<<DateEntrySelected>>", self.update_available_banquet_halls)
        self.checkout_entry.bind("<<DateEntrySelected>>", self.update_price)
        self.room_type.bind("<<ComboboxSelected>>", self.update_people_choices)
        self.num_people.bind("<<ComboboxSelected>>", self.update_price)
        
        # 宴会オプション
        banquet_section, self.banquet_var, self.banquet_check, self.banquet_choice, self.banquet_choice_label, self.drinks_var, self.drinks_check = ui_components.create_banquet_section(input_frame)
        
        # イベントバインド
        self.banquet_check.config(command=self.toggle_banquet)
        self.drinks_check.config(command=self.update_price)
        
        # 右側 - 料金情報
        price_frame, self.nights_label, self.price_label, self.price_details = ui_components.create_price_section(content_frame)
        
        # 予約ボタン
        button_frame, self.book_button = ui_components.create_button_section(self.root)
        self.book_button.config(command=self.book_room)
        
        # 予約リスト
        list_frame, self.reservations_listbox = ui_components.create_reservation_list(self.root)
        
    def update_people_choices(self, event=None):
        """部屋タイプに応じて選択可能な人数を更新"""
        room = self.room_type.get()
        if room:
            max_people = self.room_model.room_capacity.get(room, 4)
            self.num_people['values'] = [str(i) for i in range(1, max_people + 1)]
            self.num_people.set("2")  # デフォルト2人
            self.update_price()

    def get_available_banquet_halls(self):
        """選択した日付で利用可能な宴会場のリストを返す"""
        checkin_date = self.checkin_entry.get_date().strftime('%Y-%m-%d')
        return self.banquet_model.get_available_halls(checkin_date)

    def update_available_banquet_halls(self, event=None):
        """日付選択時に利用可能な宴会場のリストを更新"""
        if self.banquet_var.get():
            available_halls = self.get_available_banquet_halls()
            self.banquet_choice['values'] = available_halls
            if self.banquet_choice.get() not in available_halls:
                self.banquet_choice.set('')
        # 宿泊日数と料金も更新
        self.update_price()

    def toggle_banquet(self):
        """宴会場オプションの切り替え時に飲み放題オプションも連動させる"""
        if self.banquet_var.get():
            available_halls = self.get_available_banquet_halls()
            self.banquet_choice['values'] = available_halls
            self.banquet_choice.config(state="readonly")
            # 飲み放題オプションを有効化
            self.drinks_check.config(state="normal")
        else:
            self.banquet_choice.set("")
            self.banquet_choice.config(state="disabled")
            # 飲み放題オプションを無効化し、選択も解除
            self.drinks_var.set(False)
            self.drinks_check.config(state="disabled")
        self.update_price()

    def calculate_nights(self):
        """宿泊日数を計算"""
        try:
            checkin = self.checkin_entry.get_date()
            checkout = self.checkout_entry.get_date()
            return calculate_nights(checkin, checkout)
        except Exception:
            return 0

    def calculate_price(self):
        """料金を計算"""
        room = self.room_type.get()
        nights = self.calculate_nights()
        people = 0
        try:
            people = int(self.num_people.get() or 0)
        except ValueError:
            people = 0
        
        if not all([room, nights > 0, people > 0]):
            return 0, "-"
        
        # 部屋の基本料金
        room_price = self.room_model.room_prices.get(room, 0)
        
        # 宿泊日数を掛ける
        room_total = room_price * nights
        
        # 宴会オプション
        banquet_total = self.banquet_model.banquet_price if self.banquet_var.get() else 0
        
        # 飲み放題オプション (宴会オプションが選択されている場合のみ有効)
        drinks_total = 0
        if self.banquet_var.get() and self.drinks_var.get():
            drinks_total = self.banquet_model.drink_price * people
        
        # 料金内訳
        details = f"基本料金: {room_price:,}円 × {nights}泊 = {room_total:,}円"
        if self.banquet_var.get():
            details += f"\n宴会オプション: {self.banquet_model.banquet_price:,}円"
            if self.drinks_var.get():
                details += f"\n飲み放題オプション: {self.banquet_model.drink_price:,}円 × {people}人 = {drinks_total:,}円"
        
        total = room_total + banquet_total + drinks_total
        details += f"\n合計: {total:,}円"
        
        return total, details

    def update_price(self, event=None):
        """料金表示を更新"""
        nights = self.calculate_nights()
        self.nights_label.config(text=f"{nights}泊" if nights > 0 else "-")
        
        total_price, details = self.calculate_price()
        self.price_label.config(text=f"{total_price:,}円" if total_price > 0 else "-")
        self.price_details.config(text=details)

    def book_room(self):
        """部屋の予約を確定する"""
        name = self.name_entry.get()
        email = self.email_entry.get()
        checkin = self.checkin_entry.get()
        checkout = self.checkout_entry.get()
        room = self.room_type.get()
        num_people = self.num_people.get()
        banquet_text = "あり" if self.banquet_var.get() else "なし"
        banquet_hall = self.banquet_choice.get() if self.banquet_var.get() else "なし"
        drinks_text = "あり" if self.banquet_var.get() and self.drinks_var.get() else "なし"
        nights = self.calculate_nights()

        # 入力検証
        if not all([name, email, checkin, checkout, room, num_people, nights > 0]):
            messagebox.showerror("エラー", "すべての項目を入力してください。チェックアウト日はチェックイン日より後である必要があります。")
            return

        if self.banquet_var.get() and not banquet_hall:
            messagebox.showerror("エラー", "宴会場を選択してください")
            return

        # 部屋の予約可能性チェック
        if self.room_model.room_availability.get(room, 0) <= 0:
            messagebox.showerror("エラー", "部屋が埋まっています。")
            return

        # 宴会場の重複チェック
        if self.banquet_var.get():
            checkin_date = self.checkin_entry.get_date().strftime('%Y-%m-%d')
            booked_halls = self.banquet_model.banquet_reservations.get(checkin_date, [])
            if banquet_hall in booked_halls:
                messagebox.showerror("エラー", f"宴会場「{banquet_hall}」は既に予約されています。別の会場を選択してください。")
                return

        # 部屋の予約処理
        self.room_model.room_availability[room] -= 1
        
        # 宴会場を予約済みにマーク
        if self.banquet_var.get():
            checkin_date = self.checkin_entry.get_date().strftime('%Y-%m-%d')
            self.banquet_model.reserve_hall(checkin_date, banquet_hall)

        # 料金計算
        price, _ = self.calculate_price()

        # 予約情報をリストに追加
        reservation_text = format_reservation_text(
            name, checkin, checkout, nights, room, price, 
            num_people, banquet_text, banquet_hall, drinks_text
        )
        self.reservation_data.add_reservation(reservation_text)
        self.reservations_listbox.insert(tk.END, reservation_text)
        
        # メール送信
        success, message = send_confirmation_email(
            name, email, checkin, checkout, room, price, num_people, 
            banquet_text, banquet_hall, drinks_text, nights
        )
        
        messagebox.showinfo("成功", "予約が完了しました！メールを送信しました。")
        
        # フォームをクリアして次の入力を受け付ける準備
        self.clear_form()
        
        # 予約完了後に利用可能な宴会場リストを更新
        self.update_available_banquet_halls()
        
    def book_room(self):
        """部屋の予約を確定し、予約情報を JSON に追加保存する"""
        name = self.name_entry.get()
        email = self.email_entry.get()
        checkin = self.checkin_entry.get()
        checkout = self.checkout_entry.get()
        room = self.room_type.get()
        num_people = self.num_people.get()
        banquet_text = "あり" if self.banquet_var.get() else "なし"
        banquet_hall = self.banquet_choice.get() if self.banquet_var.get() else "なし"
        drinks_text = "あり" if self.banquet_var.get() and self.drinks_var.get() else "なし"
        nights = self.calculate_nights()

        # 予約情報を辞書にまとめる
        reservation = {
            "name": name,
            "email": email,
            "checkin": checkin,
            "checkout": checkout,
            "room": room,
            "num_people": num_people,
            "banquet": {
                "status": banquet_text,
                "hall": banquet_hall,
                "drinks": drinks_text
            },
            "nights": nights
        }

        # 既存の予約情報を読み込む
        try:
            with open("hotel_booking_app.json", "r", encoding="utf-8") as f:
                reservations = json.load(f)
            # JSONファイルの内容が辞書の場合はリストに変換
            if isinstance(reservations, dict):
                reservations = [reservations]
        except (FileNotFoundError, json.JSONDecodeError):
            reservations = []  # ファイルが存在しないか読み込みエラーが起きた場合

        # 新しい予約情報をリストに追加
        reservations.append(reservation)

        # 予約情報をファイルに上書き保存（追加済みの全ての予約情報を保存）
        try:
            with open("hotel_booking_app.json", "w", encoding="utf-8") as f:
                json.dump(reservations, f, ensure_ascii=False, indent=4)
            print("予約情報を hotel_booking_app.json に追加保存しました。")
        except Exception as e:
            print("予約情報の保存中にエラーが発生しました:", e)

    def clear_form(self):
        """フォームをクリアする"""
        self.name_entry.delete(0, tk.END)
        self.email_entry.delete(0, tk.END)
        self.room_type.set("")
        self.num_people.set("")
        self.banquet_var.set(False)
        self.drinks_var.set(False)
        self.toggle_banquet()
        # 日付はリセットしない（ユーザーが同じ日付で別の予約をする可能性があるため）