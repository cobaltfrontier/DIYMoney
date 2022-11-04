from app.db_connect import connect

def update_password(user_id, encrypted_password_string):
    conn = connect()
    with conn.cursor() as cur:
        sql = f'UPDATE user SET password = "{encrypted_password_string}" WHERE id like {user_id};'
        try:
            cur.execute(sql)
            conn.commit()
        except:
            print("Didn't work")

def update_avatar(user_id, avatar):
    conn = connect()
    with conn.cursor() as cur:
        sql = f'UPDATE user SET avatar = "{avatar}" WHERE id like {user_id};'
        try:
            cur.execute(sql)
            conn.commit()
        except:
            print("Didn't work")

def create_user(form_username, form_password, form_email, form_first_name, form_last_name, form_avatar):
    conn = connect()
    with conn.cursor() as cur:
        sql = f'INSERT INTO user (username, password, email, first_name, last_name, avatar) VALUES ({form_username}, {form_password}, {form_email}, {form_first_name}, {form_last_name}, {form_avatar});'
        try:
            cur.execute(sql)
            conn.commit()
        except:
            print("Didn't work")

