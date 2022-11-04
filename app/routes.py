from flask import render_template,  redirect, url_for, flash, session, request
from app.forms import LoginForm
from app.forms import AssetClassForm, TickerForm, ProfileForm, TaxForm
from app import app, db
from app.models import User, AssetClass, Ticker
from flask_login import login_user, logout_user, current_user, login_required, LoginManager
from app.formatting import *
from app.functions import *
from app.update_ticker import *
from cryptography.fernet import Fernet
from app.update_profile import *
from app.password_testing import *
from app.chart_data import *

#password = '1234'
#byte_password = bytes(password, 'utf-8')
#key = Fernet.generate_key()
#print(key)
#crypter = Fernet(key)
#pw = crypter.encrypt(byte_password)
#decryptString = crypter.decrypt(pw)
#print(str(decryptString, 'utf-8'))
#print(str(pw, 'utf-8'))

#if form_password != None:


@app.route('/')
def index():
    title = "Welcome to DIY Money"
    return render_template('index.html', title=title)

@app.route('/about')
def about():
     header = "About DIY Money"
     return render_template('about.html', header=header)

@app.route('/contact')
def contact():
     top_text = "Get in touch"
     return render_template('contact.html', top_text=top_text)

##### USER MANAGEMENT ##### FOUND: https://www.youtube.com/watch?v=2dEM-s3mRLE
login_manager = LoginManager()
login_manager.init_app(app)

# This method is used to as part of the flask_login code.
@login_manager.user_loader
def load_user(user_id):
     return User.query.get(int(user_id))

@app.route('/login', methods=['GET', 'POST'])
def login():
     if current_user.is_authenticated:
          return redirect(url_for('index'))
     form = LoginForm()
     # set form data to variables
     form_username = form.username.data
     form_password = form.password.data
     if form.validate_on_submit():
          user = User.query.filter_by(username=form_username).first()

          encrypted_password = user.password
          byte_password = bytes(encrypted_password, 'utf-8')

          decrypted_password_string = decrypt_password(byte_password)

          if user is None or form_password != decrypted_password_string:
               flash(f'Invalid username or passsword key: encrypted password string:  decrypted password string: {decrypted_password_string}')
               return redirect(url_for('login'))
          login_user(user, remember=form.remember_me.data)

          session.permanent = True
          session['first_name'] = user.first_name
          session['last_name'] = user.last_name
          session['id'] = user.id
          session['username'] = user.username
          session['avatar'] = user.avatar
          session['email'] = user.email
          return redirect(url_for('dashboard'))
     return render_template('login.html',  title='Sign In', form=form)

@app.route('/dashboard')
def dashboard():
     first_name = session['first_name']
     last_name = session['last_name']
     username = session['username']
     avatar = session['avatar']
     email = session['email']
     user_id = session['id']
     return render_template('dashboard.html', first_name=first_name, user_id=user_id, email=email, avatar=avatar, username=username, last_name=last_name)

### LOGIN STUFF ###
@app.route('/logout')
@login_required
def logout():
     logout_user()
     return redirect(url_for('index'))

#this route redirects unauthorized users to the login page.
@login_manager.unauthorized_handler
def unauthorized():
     # do stuff
     return redirect(url_for('login'))

@app.route('/asset_class', methods=['GET', 'POST'])
@login_required
def asset_class():
     form = AssetClassForm()
     if request.method == 'POST':
          asset_class_name = request.form.get("asset_class_name")
          allocation_percent = request.form.get("allocation_percent")
          user_id = session['id']
          asset_class = AssetClass(asset_class_name=asset_class_name, allocation_percent=allocation_percent, user_id=user_id)
          db.session.add(asset_class)
          db.session.commit()
          return redirect(url_for('asset_class'))
     user_id = session['id']
     asset_classes = get_asset_class(user_id)
     label, data = get_chart_data_asset_classes(user_id)
     #this is a join.. the item in the join section is the left side of the table
     return render_template('asset_class.html', form=form, user_id=user_id,
                            asset_classes=asset_classes, label=label, data=data)

#@app.route('/asset_class_update/<asset_class_id>/', methods=['GET', 'POST'])
#@login_required
#def asset_class_update(asset_class_id):
#     form = AssetClassForm()
#     if request.method == 'POST':
#          asset_class_data = AssetClass.query.get(asset_class_id)
#          asset_class_data.asset_class_name = form.asset_class_name.data
#          asset_class_data.allocation_percent = form.allocation_percent.data
#          db.session.commit()
#          return redirect(url_for('asset_class'))
#     return render_template('asset_class.html', form=form)

@app.route('/asset_class_update/<asset_class_id>/',  methods=['GET', 'POST'])
def asset_class_update(asset_class_id):
        asset_class_data = AssetClass.query.get(asset_class_id)
        asset_class_data.asset_class_name = request.form.get("asset_class_name")
        asset_class_data.allocation_percent = request.form.get("allocation_percent")
        db.session.commit()
#        flash(f"{asset_class.asset_class_name} has been updated.")
        return redirect(url_for('asset_class'))
        return render_template('asset_class.html', form=form)

#@app.route('/asset_class_delete/<asset_class_id>/', methods=['GET', 'POST'])
#@login_required
#def asset_class_delete(asset_class_id):
#     asset_class_data = AssetClass.query.get(asset_class_id)
     ##Doing it this way extends the foreign key relationship to delete in the db all related "cascade delete"
     ## Add synchronize session to refresh the session on the view, otherwise you get an error
#     db.session.query(AssetClass).filter(AssetClass.asset_class_id==asset_class_id).delete(synchronize_session='fetch')
#     db.session.commit()
#     flash(f"{asset_class_data.asset_class_name} has been deleted.")
#     return redirect(url_for('asset_class'))

@app.route('/asset_class_delete/<asset_class_id>/', methods=['GET', 'POST'])
def asset_class_delete(asset_class_id):
     db.session.query(AssetClass).filter(AssetClass.asset_class_id==asset_class_id).delete()
     db.session.commit()
     flash(f"this has been deleted.")
     return redirect(url_for('asset_class'))

@app.route('/ticker', methods=['GET', 'POST'])
@login_required
def ticker():
    form = TickerForm()
    user_id = session['id']
    asset_classes = get_asset_class(user_id)

    #goes in the dictionary asset_classes and iterates through each row, asset_class and gets asset_class_id and asset_class_name to create the asset class choices
    form.asset_class.choices = [(asset_class['asset_class_id'], asset_class['asset_class_name']) for asset_class in asset_classes]

    if request.method == 'POST':
        ticker_symbol = request.form.get('ticker_symbol')
        company_name = request.form.get('company_name')
        #current_price = request.form.get("current_price")
        asset_class_id = request.form.get('asset_class')
        user_id = session['id']
        ticker = Ticker(ticker_symbol=ticker_symbol, company_name=company_name, asset_class_id=asset_class_id, user_id=user_id)
        db.session.add(ticker)
        db.session.commit()
        return redirect(url_for('ticker'))
    user_id = session['id']
    tickers = get_tickers(user_id)
    return render_template('ticker.html', form=form, asset_classes=asset_classes, tickers=tickers)

@app.route('/ticker_update/<ticker_id>/', methods=['GET', 'POST'])
@login_required
def ticker_update(ticker_id):
    #form = TickerForm()
    ticker = Ticker.query.get(ticker_id)
    ticker.ticker_symbol = request.form.get('ticker_symbol')
    ticker.company_name = request.form.get('company_name')
    ticker.asset_class_id = request.form.get('asset_class')
    db.session.commit()
    flash(f"{ticker.ticker_symbol} has been updated.")
    return redirect(url_for('ticker'))
    #return render_template('ticker.html', form=form)

@app.route('/ticker_delete/<ticker_id>/', methods=['GET', 'POST'])
@login_required
def ticker_delete(ticker_id):
    db.session.query(Ticker).filter(Ticker.ticker_id==ticker_id).delete()
    db.session.commit()
    flash(f"This has been deleted.")
    return redirect(url_for('ticker'))

@app.route('/ticker_price_update', methods=['GET', 'POST'])
@login_required
def ticker_price_update():
    post_ticker_prices()
    return redirect(url_for('ticker'))


@app.route('/profile_password', methods=['GET', 'POST'])
@login_required
def profile_password():
     form = ProfileForm()
     user_id = session['id']
     user = get_user(user_id)
     email = user[0]['email']
     # set form data to variables
     if request.method == 'POST':
        form_username = form.username.data
        form_password = form.password.data
        form_email = form.email.data
        form_first_name = form.first_name.data
        form_last_name = form.last_name.data
        form_avatar = form.avatar.data
        user_id = session['id']

        encrypted_password_string = encrypt_password(form_password)

        update_password(user_id, encrypted_password_string)

        flash(f"{form_password} has been updated.")

     return render_template('profile_password.html',  title='profile', form=form, user=user, email=email)

@app.route('/update_avatar', methods=['GET', 'POST'])
@login_required
def update_avatar():
     form = ProfileForm()
     user_id = session['id']
     user = get_user(user_id)
     avatar = user[0]['avatar']
     # set form data to variables
     if request.method == 'POST':
        user = User.query.get(user_id)
        form_avatar = form.avatar.data
        #form_file = form..data
        user.avatar = form_avatar
        db.session.commit()
        return redirect(url_for('update_avatar'))
     return render_template('update_avatar.html',  title='update avatar', form=form, avatar=avatar)

@app.route('/create_user', methods=['GET', 'POST'])
def create_user():
     form = ProfileForm()
     # set form data to variables
     if request.method == 'POST':
        form_username = form.username.data
        form_password = form.password.data
        form_email = form.email.data
        form_first_name = form.first_name.data
        form_last_name = form.last_name.data
        form_avatar = form.avatar.data
        user_id = session['id']
        form_password = encrypt_password(form_password)
        user = User(username= form_username, password=form_password, email=form_email, first_name=form_first_name, last_name=form_last_name, avatar=form_avatar)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('create_user'))
     return render_template('create_user.html',  title='create user', form=form)

#New 6/6/2022
@app.route('/tax_calculator_page', methods=['GET', 'POST'])
@login_required
def tax_calculator_page():
    test_variable = "Test Variable"
    form = TaxForm()
    Single = "1 - Single"
    Married = "2 - Married"
    form.marital_status.choices = [Single, Married]
    # set form data to variables
    if request.method == 'POST':
        form_total_wages = form.total_wages.data
        form_marital_status = form.marital_status.data
        form_total_taxes_paid = form.total_taxes_paid.data
        taxes_owed = calculate_taxes(form_total_wages, form_marital_status)
        print(taxes_owed)
        user_id = session['id']
        #time to store the taxes owed in the database so that when the page starts up it will have a way of showing the value
        #user = User.query.get(user_id)
        #could possiby do an if statement and say, if positive then store as tax return in the database
        #but could set taxes owed to null or 0
        #but the question would be how to display a header saying, you owe this much or alternatively your tax return is this much
        #user.taxes_owed = taxes_owed
        #db.session.commit()
        return redirect(url_for('tax_calculator_page'))
    return render_template('tax_calculator_page.html', title='create user', form=form, test_variable=test_variable)











