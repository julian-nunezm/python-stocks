import json, datetime

def print_as_json(dict):
    print(json.dumps(dict, indent=4))

def organise_tickers_by_sector(tickers):
    tickers_by_sector = {}
    for ticker in tickers:
        sector_key = ticker.get_general_info().get('Sector')
        if sector_key:
            if not sector_key in tickers_by_sector.keys():
                tickers_by_sector[sector_key] = {}
            industry_key = ticker.get_general_info().get('Industry')
            if industry_key:
                value = ticker
                if industry_key in tickers_by_sector[sector_key].keys():
                    tickers_by_sector[sector_key][industry_key].append(value)
                else:
                    tickers_by_sector[sector_key][industry_key] = [value]
    return tickers_by_sector

#def cast_datetime_to_date(value):
#    return date