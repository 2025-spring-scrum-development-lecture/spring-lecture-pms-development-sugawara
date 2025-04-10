import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime

def calculate_nights(checkin_date, checkout_date):
    """宿泊日数を計算"""
    if checkout_date <= checkin_date:
        return 0
    return (checkout_date - checkin_date).days

def send_confirmation_email(name, email, checkin, checkout, room, price, num_people, 
                          banquet_text, banquet_hall, drinks_text, nights):
    """予約確認メールを送信する"""
    msg = MIMEMultipart()
    msg["From"] = "yourhotel@example.com"
    msg["To"] = email
    msg["Subject"] = "ホテル予約確認"
    body = f"""
{name} 様

以下の内容で予約を承りました：

チェックイン: {checkin}
チェックアウト: {checkout}
宿泊日数: {nights}泊
部屋: {room}
人数: {num_people}
料金: {price:,}円
宴会オプション: {banquet_text}
宴会場: {banquet_hall if banquet_text == 'あり' else 'なし'}
飲み放題: {drinks_text}

ご利用ありがとうございます。
"""
    msg.attach(MIMEText(body, "plain"))

    try:
        # 下記はSMTP設定の例。実運用では環境に応じて設定してください。
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login("t.inakawa.sys24@morijyobi.ac.jp", "rukf tmia oemd wcla")
            server.send_message(msg)
        return True, "メール送信成功"
    except Exception as e:
        return False, f"メール送信失敗: {e}"

def format_reservation_text(name, checkin, checkout, nights, room, price, 
                          num_people, banquet_text, banquet_hall, drinks_text):
    """予約情報をテキスト形式でフォーマット"""
    return f"{name}: {checkin} - {checkout} ({nights}泊), {room} ({price:,}円), 人数: {num_people}, 宴会: {banquet_text}（{banquet_hall}）, 飲み放題: {drinks_text}"