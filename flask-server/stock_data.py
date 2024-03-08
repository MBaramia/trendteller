from db_schema import Prediction, HistoricData

def get_prediction_data(company_id, timeframe):
    prediction_data = Prediction.query.filter_by(companyID=company_id, timeframe=timeframe).all()
    data_list = [{
        'date_predicted': item.date_predicted.strftime("%Y-%m-%d %H:%M:%S"),
        'open': item.open,
        'high': item.high,
        'low': item.low,
        'close': item.close,
        'volume': item.volume,
        'timeframe': item.timeframe
    } for item in prediction_data]
    return data_list

def get_historic_data(company_id, timeframe):
    historic_data = HistoricData.query.filter_by(companyID=company_id, timeframe=timeframe).all()
    data_list = [{
        'date': item.date.strftime("%Y-%m-%d %H:%M:%S"),
        'open': item.open,
        'high': item.high,
        'low': item.low,
        'close': item.close,
        'volume': item.volume,
        'timeframe': item.timeframe
    } for item in historic_data]
    return data_list

print(get_historic_data(0, "daily"))