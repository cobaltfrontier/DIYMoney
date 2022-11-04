from app import db, app
from app.db_connect import connect

def get_asset_class(user_id):
        conn = connect()
        with conn.cursor() as cur:
            sql = f'SELECT asset_class_id, asset_class_name, allocation_percent, user_id from asset_class WHERE user_id = { user_id } '
            cur.execute(sql)
            return cur.fetchall()

def get_tickers(user_id):
    conn = connect()
    with conn.cursor() as cur:
        sql = f'SELECT t.ticker_id, t.ticker_symbol, t.company_name, t.current_price, ac.asset_class_id, ac.asset_class_name, t.user_id ' \
              f'from ticker t ' \
              f'JOIN asset_class ac ON t.asset_class_id=ac.asset_class_id ' \
              f'WHERE t.user_id = { user_id };'
        cur.execute(sql)
        return cur.fetchall()

def get_user(user_id):
    conn = connect()
    with conn.cursor() as cur:
        sql = f'SELECT id, username, password, email, first_name, last_name, avatar from user WHERE id = { user_id }'
        cur.execute(sql)
        return cur.fetchall()

def get_asset_class_chart(user_id):
    conn = connect()
    with conn.cursor() as cur:
        sql = f'SELECT asset_class_name, allocation_percent from asset_class WHERE user_id = { user_id }'
        cur.execute(sql)
        return cur.fetchall()


# This is a module.
# You can define variables and functions here, and use them from any form. For example, in a top-level form:
#
#    from . import Module1
#
#    Module1.say_hello()
#

# This defines the main function and takes in arguments total_wages, taxes_paid and marital_status
def calculate_taxes(total_wages, marital_status):
    # if marital status is single
    if marital_status == "1 - Single":
        # standard deduction then equals 12,200
        standard_deduction = 12200
    # or else
    else:
        # standard deduction equals 24,400
        standard_deduction = 24400

    # calculates adjusted gross income as total_wages - standard_deduction
    a_g_i = total_wages - standard_deduction

    # defines taxable_income as a_g_i
    taxable_income = a_g_i

    # checks if marital status is single
    if marital_status == "1 - Single":
        # checks if taxable income is less than or equal to 9875
        if taxable_income <= 9875:
            # taxes = .10  of taxable_income
            taxes = .10 * taxable_income
        # checks if taxable income is less than or equal to 9875
        elif taxable_income <= 40125:
            # taxes = 987.50 + (.12 * (taxable_income - 9875))
            taxes = 987.50 + (.12 * (taxable_income - 9875))
        # checks if taxable income is less than or equal to 40125
        elif taxable_income <= 85525:
            # taxes = 4617.50 + (.22 * (taxable_income - 40125))
            taxes = 4617.50 + (.22 * (taxable_income - 40125))
        # checks if taxable income is less than or equal to 85525
        elif taxable_income <= 163300:
            # taxes = 14605.50 + (.24 * (taxable_income - 85525))
            taxes = 14605.50 + (.24 * (taxable_income - 85525))
        # checks if taxable income is less than or equal to 163300
        elif taxable_income <= 207350:
            # taxes = 33271.50 + (.32 * (taxable_income - 163300))
            taxes = 33271.50 + (.32 * (taxable_income - 163300))
        # checks if taxable income is less than or equal to 207350
        elif taxable_income <= 518400:
            # taxes = 47367.50 + (.35 * (taxable_income - 207350))
            taxes = 47367.50 + (.35 * (taxable_income - 207350))
        # checks if taxable income is more than or equal to 518401
        elif taxable_income >= 518401:
            # taxes = 156235 + (.37 * (taxable_income - 518400))
            taxes = 156235 + (.37 * (taxable_income - 518400))
    # else (if marital status is married)
    else:
        # checks if taxable income is less than or equal to 19750
        if taxable_income <= 19750:
            # taxes = .10 * taxable_income
            taxes = .10 * taxable_income
        # checks if taxable income is less than or equal to 80250
        elif taxable_income <= 80250:
            # taxes = 1975 + (.12 * (taxable_income - 19750))
            taxes = 1975 + (.12 * (taxable_income - 19750))
        # checks if taxable income is less than or equal to 171050
        elif taxable_income <= 171050:
            # taxes = 9235 + (.22 * (taxable_income - 80250))
            taxes = 9235 + (.22 * (taxable_income - 80250))
        # checks if taxable income is less than or equal to 326600
        elif taxable_income <= 326600:
            # taxes = 29211 + (.24 * (taxable_income - 171050))
            taxes = 29211 + (.24 * (taxable_income - 171050))
        # checks if taxable income is less than or equal to 414700
        elif taxable_income <= 414700:
            # taxes = 66543 + (.32 * (taxable_income - 326600))
            taxes = 66543 + (.32 * (taxable_income - 326600))
        # checks if taxable income is less than or equal to 622050
        elif taxable_income <= 622050:
            # taxes = 94735 + (.35 * (taxable_income - 414700))
            taxes = 94735 + (.35 * (taxable_income - 414700))
        # checks if taxable income is more than or equal to 622051
        elif taxable_income >= 622051:
            # taxes = 167307.50 + (.37 * (taxable_income - 622050))
            taxes = 167307.50 + (.37 * (taxable_income - 622050))

    # return taxes
    return taxes





