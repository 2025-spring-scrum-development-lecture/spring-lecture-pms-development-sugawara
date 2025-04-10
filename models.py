class RoomModel:
    def __init__(self):
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
        
        # 部屋の利用可能数
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


class BanquetModel:
    def __init__(self):
        self.banquet_price = 10000  # 宴会場の基本料金
        self.drink_price = 2800     # 飲み放題の一人あたり料金
        self.banquet_halls = ["春日", "平安", "末広", "芙蓉", "蘭", "桜", "岩鷲"]
        # 宴会場の予約状況を管理する辞書
        self.banquet_reservations = {}
    
    def get_available_halls(self, date_str):
        """指定した日付で利用可能な宴会場のリストを返す"""
        booked_halls = self.banquet_reservations.get(date_str, [])
        return [hall for hall in self.banquet_halls if hall not in booked_halls]
    
    def reserve_hall(self, date_str, hall_name):
        """宴会場を予約する"""
        if date_str not in self.banquet_reservations:
            self.banquet_reservations[date_str] = []
        self.banquet_reservations[date_str].append(hall_name)


class ReservationData:
    def __init__(self):
        self.reservations = []
    
    def add_reservation(self, reservation):
        self.reservations.append(reservation)
        return len(self.reservations) - 1  # 予約番号を返す