from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField, FloatField
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

## ASSET CLASS ##
class AssetClassForm(FlaskForm):
    asset_class_name = StringField('Asset Class Name', validators=[DataRequired()])
    allocation_percent = StringField('Allocation Percent', validators=[DataRequired()])
    submit = SubmitField('Submit')

class TickerForm(FlaskForm):
    ticker_symbol = StringField('Ticker Symbol', validators=[DataRequired()])
    company_name = StringField('Company Name', validators=[DataRequired()])
    #current_price = StringField('Current Price', validators=[DataRequired()])
    asset_class = SelectField('Asset Class', choices=[])
    submit = SubmitField('Submit')

class ProfileForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired()])
    first_name = StringField('First_name', validators=[DataRequired()])
    last_name = StringField('Last_name', validators=[DataRequired()])
    avatar = StringField('Avatar', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Change Information')

#new 6/6/2022
class TaxForm(FlaskForm):
    total_wages = FloatField('Total Wages', validators=[DataRequired()])
    total_taxes_paid = FloatField('Total Taxes Paid', validators=[DataRequired()])
    marital_status = SelectField('Marital Status', choices=[])
    submit = SubmitField('Submit')

