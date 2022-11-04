from app.functions import *
from app.decimalencoder import *
import json


def get_chart_data_asset_classes(user_id):
    asset_classes = get_asset_class_chart(user_id)

    #create two lists for label and data
    label = []
    value = []

    for asset_class in asset_classes:
        label.append(asset_class['asset_class_name'])
        value.append(asset_class['allocation_percent'])

    a_class = json.dumps(label, indent=4, sort_keys=True, default=str)
    a_percent = json.dumps(value, cls=DecimalEncoder) # The list has issues with decimals. This converter fixes it

    return a_class, a_percent
