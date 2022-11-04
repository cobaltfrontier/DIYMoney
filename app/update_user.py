from app import db, app
from app.db_connect import connect

def get_user_id():
    conn = connect()
    with conn.cursor() as cur:
        sql = f'SELECT id  '\
              f'from user'
        cur.execute(sql)
        return cur.fetchall()

def update_user(new_password, user):
    conn = connect()
    with conn.cursor() as cur:
        sql = f'UPDATE user SET password = {new_password} WHERE username like {user_id};'
        try:
            cur.execute(sql)
            conn.commit()
        except:
            print("Didn't work")

def update_password(user_id, new_password):
    conn = connect()
    with conn.cursor() as cur:
        sql = f'UPDATE user SET username = {new_password} WHERE id like "{user_id}";'
        try:
            cur.execute(sql)
            conn.commit()
        except:
            print("Didn't work")

def update_first_and_last(user_id, new_password):
    conn = connect()
    with conn.cursor() as cur:
        sql = f'UPDATE user SET username = {new_password} WHERE id like "{user_id}";'
        try:
            cur.execute(sql)
            conn.commit()
        except:
            print("Didn't work")

def update_email(user_id, new_password):
    conn = connect()
    with conn.cursor() as cur:
        sql = f'UPDATE user SET username = {new_password} WHERE id like "{user_id}";'
        try:
            cur.execute(sql)
            conn.commit()
        except:
            print("Didn't work")

def update_avatar(user_id, new_password):
    conn = connect()
    with conn.cursor() as cur:
        sql = f'UPDATE user SET username = {new_password} WHERE id like "{user_id}";'
        try:
            cur.execute(sql)
            conn.commit()
        except:
            print("Didn't work")

def post_ticker_prices():
    users = get_user_id()
    for user in users:
        user_username = user['username']
        user_password = user['password']
        user_email = user['email']
        user_id = user['id']
        if symbol == "CASH":
            price = 1
        else:
            price = get_stock_price(ticker['ticker_symbol'])
            print(f"{symbol} {price}")
            update_price(symbol, price)
