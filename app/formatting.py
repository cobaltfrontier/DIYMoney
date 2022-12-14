from app import app

@app.template_filter()
def percentageFormat(value):
    value = float(value)
    return f"{value:,.2f}%"

@app.template_filter()
def moneyFormat(value):
    value = float(value)
    return f"${value:,.2f}"
