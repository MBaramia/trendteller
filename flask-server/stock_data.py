from db_schema import Prediction, HistoricData
from datetime import datetime
from sqlalchemy import text
from db_schema import db

def get_prediction_data(company_id, timeframe):
    # prediction_data = Prediction.query.filter_by(companyID=company_id, timeframe=timeframe).all()

    # SQL query to fetch prediction data
    getPredictionQuery = text("""
        SELECT date_predicted, open, high, low, close, volume, timeframe
        FROM Prediction 
        WHERE companyID = :companyId AND timeframe = :timeframe
    """)
    getPredictionQuery = getPredictionQuery.bindparams(companyId=company_id, timeframe=timeframe)
    results = db.session.execute(getPredictionQuery)
    prediction_data = results.fetchall()

    data_list = [{
        'date_predicted': datetime.strptime(item[0], "%Y-%m-%d %H:%M:%S.%f").strftime("%Y-%m-%d %H:%M:%S"),
        'open': item[1],
        'high': item[2],
        'low': item[3],
        'close': item[4],
        'volume': item[5],
        'timeframe': item[6]
    } for item in prediction_data]
    return data_list

def get_historic_data(company_id, timeframe):
    # historic_data = HistoricData.query.filter_by(companyID=company_id, timeframe=timeframe).all()

    getHistoricQuery = text("""
        SELECT date, open, high, low, close, volume, timeframe
        FROM HistoricData
        WHERE companyID = :companyId AND timeframe = :timeframe
    """)
    getHistoricQuery = getHistoricQuery.bindparams(companyId=company_id, timeframe=timeframe)
    results = db.session.execute(getHistoricQuery)
    historic_data = results.fetchall()

    data_list = [{
        'date': datetime.strptime(item[0], "%Y-%m-%d %H:%M:%S.%f").strftime("%Y-%m-%d %H:%M:%S"),
        'open': item[1],
        'high': item[2],
        'low': item[3],
        'close': item[4],
        'volume': item[5],
        'timeframe': item[6]
    } for item in historic_data]
    return data_list

def get_prediction_data_formatted(company_id):
    timeframes = ["intraday", "daily", "weekly", "monthly"]
    result = {
        0: {},
        1: {},
        2: {},
        3: {}
    }
    for i, timeframe in enumerate(timeframes):
        data_points = get_prediction_data(company_id, timeframe)
        for data in data_points:
            result[i][data["date_predicted"]] = {
                "open": data["open"],
                "high": data["high"],
                "low": data["low"],
                "close": data["close"],
                "volume": data["volume"],
                "isPrediction": True
            }
    return result

def get_historic_data_formatted(company_id):
    timeframes = ["intraday", "daily", "weekly", "monthly"]
    result = {
        0: {},
        1: {},
        2: {},
        3: {}
    }
    for i, timeframe in enumerate(timeframes):
        data_points = get_historic_data(company_id, timeframe)
        for data in data_points:
            result[i][data["date"]] = {
                "open": data["open"],
                "high": data["high"],
                "low": data["low"],
                "close": data["close"],
                "volume": data["volume"],
                "isPrediction": False
            }
    return result

def get_combined_stock_data(company_id):
    historic = get_historic_data_formatted(company_id)
    prediction = get_prediction_data_formatted(company_id)
    combinedData = {
        outer_key: {**historic.get(outer_key, {}), **prediction.get(outer_key, {})}
        for outer_key in set(historic) | set(prediction)
    }
    return combinedData

def get_historic_stock_dates(company_id):
    dates = [[], [], [], []]
    historic = get_historic_data_formatted(company_id)

    for outer_key, inner_dict in historic.items():
        dates[outer_key] = sorted(inner_dict.keys(), key=lambda date: datetime.strptime(date, "%Y-%m-%d %H:%M:%S") if ' ' in date else datetime.strptime(date, "%Y-%m-%d"), reverse=True)
    
    return dates

def get_prediction_stock_dates(company_id):
    dates = [[], [], [], []]
    prediction = get_prediction_data_formatted(company_id)

    for outer_key, inner_dict in prediction.items():
        dates[outer_key] = sorted(inner_dict.keys(), key=lambda date: datetime.strptime(date, "%Y-%m-%d %H:%M:%S") if ' ' in date else datetime.strptime(date, "%Y-%m-%d"), reverse=True)
    
    return dates

def get_main_stock_data(company_id):
    date = get_historic_stock_dates(company_id)[0][0]
    historic = get_historic_data_formatted(company_id)[0][date]
    historic["price"] = historic["close"]
    return historic

def get_1D_change(company_id):
    today_now_datetime = get_historic_stock_dates(company_id)[0][0]
    yesterday_close_datetime = get_historic_stock_dates(company_id)[1][0]
    today_price = get_historic_data_formatted(company_id)[0][today_now_datetime]["close"]
    yesterday_price = get_historic_data_formatted(company_id)[1][yesterday_close_datetime]["close"]
    change = today_price - yesterday_price
    change = round(change, 2)
    percentage = (change / yesterday_price) * 100
    percentage = round(percentage, 2)
    change = f"+{change}" if (change > 0) else change
    return (change, percentage)

def get_1W_change(company_id):
    today_now_datetime = get_historic_stock_dates(company_id)[0][0]
    last_week_datetime = get_historic_stock_dates(company_id)[2][0]
    today_price = get_historic_data_formatted(company_id)[0][today_now_datetime]["close"]
    last_week_price = get_historic_data_formatted(company_id)[2][last_week_datetime]["close"]
    change = today_price - last_week_price
    change = round(change, 2)
    percentage = (change / last_week_price) * 100
    percentage = round(percentage, 2)
    change = f"+{change}" if (change > 0) else change
    return (change, percentage)

def get_1M_change(company_id):
    today_now_datetime = get_historic_stock_dates(company_id)[0][0]
    last_month_datetime = get_historic_stock_dates(company_id)[3][0]
    today_price = get_historic_data_formatted(company_id)[0][today_now_datetime]["close"]
    last_month_price = get_historic_data_formatted(company_id)[3][last_month_datetime]["close"]
    change = today_price - last_month_price
    change = round(change, 2)
    percentage = (change / last_month_price) * 100
    percentage = round(percentage, 2)
    change = f"+{change}" if (change > 0) else change
    return (change, percentage)

def get_3M_change(company_id):
    today_now_datetime = get_historic_stock_dates(company_id)[0][0]
    month_datetime = get_historic_stock_dates(company_id)[3][2]
    today_price = get_historic_data_formatted(company_id)[0][today_now_datetime]["close"]
    month_price = get_historic_data_formatted(company_id)[3][month_datetime]["close"]
    change = today_price - month_price
    change = round(change, 2)
    percentage = (change / month_price) * 100
    percentage = round(percentage, 2)
    change = f"+{change}" if (change > 0) else change
    return (change, percentage)

def get_6M_change(company_id):
    today_now_datetime = get_historic_stock_dates(company_id)[0][0]
    historic_dates = get_historic_stock_dates(company_id)
    month_datetime = historic_dates[3][5 % len(historic_dates[3])]
    today_price = get_historic_data_formatted(company_id)[0][today_now_datetime]["close"]
    month_price = get_historic_data_formatted(company_id)[3][month_datetime]["close"]
    change = today_price - month_price
    change = round(change, 2)
    percentage = (change / month_price) * 100
    percentage = round(percentage, 2)
    change = f"+{change}" if (change > 0) else change
    return (change, percentage)

def get_1Y_change(company_id):
    today_now_datetime = get_historic_stock_dates(company_id)[0][0]
    historic_dates = get_historic_stock_dates(company_id)
    month_datetime = historic_dates[3][11 % len(historic_dates[3])]
    today_price = get_historic_data_formatted(company_id)[0][today_now_datetime]["close"]
    month_price = get_historic_data_formatted(company_id)[3][month_datetime]["close"]
    change = today_price - month_price
    change = round(change, 2)
    percentage = (change / month_price) * 100
    percentage = round(percentage, 2)
    change = f"+{change}" if (change > 0) else change
    return (change, percentage)

def get_2Y_change(company_id):
    today_now_datetime = get_historic_stock_dates(company_id)[0][0]
    historic_dates = get_historic_stock_dates(company_id)
    month_datetime = historic_dates[3][23 % len(historic_dates[3])]
    today_price = get_historic_data_formatted(company_id)[0][today_now_datetime]["close"]
    month_price = get_historic_data_formatted(company_id)[3][month_datetime]["close"]
    change = today_price - month_price
    change = round(change, 2)
    percentage = (change / month_price) * 100
    percentage = round(percentage, 2)
    change = f"+{change}" if (change > 0) else change
    return (change, percentage)

def get_max_change(company_id):
    today_now_datetime = get_historic_stock_dates(company_id)[0][0]
    historic_dates = get_historic_stock_dates(company_id)
    month_datetime = historic_dates[3][-1]
    today_price = get_historic_data_formatted(company_id)[0][today_now_datetime]["close"]
    month_price = get_historic_data_formatted(company_id)[3][month_datetime]["close"]
    change = today_price - month_price
    change = round(change, 2)
    percentage = (change / month_price) * 100
    percentage = round(percentage, 2)
    change = f"+{change}" if (change > 0) else change
    return (change, percentage)

def get_changes_data(company_id):
    data = {
        "data": [
            f"{get_1D_change(company_id)[0]} ({get_1D_change(company_id)[1]}%)",
            f"{get_1W_change(company_id)[0]} ({get_1W_change(company_id)[1]}%)",
            f"{get_1M_change(company_id)[0]} ({get_1M_change(company_id)[1]}%)",
            f"{get_3M_change(company_id)[0]} ({get_3M_change(company_id)[1]}%)",
            f"{get_6M_change(company_id)[0]} ({get_6M_change(company_id)[1]}%)",
            f"{get_1Y_change(company_id)[0]} ({get_1Y_change(company_id)[1]}%)",
            f"{get_2Y_change(company_id)[0]} ({get_2Y_change(company_id)[1]}%)",
            f"{get_max_change(company_id)[0]} ({get_max_change(company_id)[1]}%)",
        ]
    }
    return data

def get_change_percentage(company_id):
    percentage = get_1D_change(company_id)[1]
    percentage = f"+{percentage}" if percentage > 0 else percentage
    return f"{percentage}%"

def get_price(company_id):
    today_now_datetime = get_historic_stock_dates(company_id)[0][0]
    today_price = get_historic_data_formatted(company_id)[0][today_now_datetime]["close"]
    return today_price